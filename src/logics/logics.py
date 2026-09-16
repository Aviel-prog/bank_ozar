import datetime
import logging
from decimal import Decimal

from src.config import SUBSCRIPTION_DATE_FORMAT
from src.exceptions import (
    AccountAlreadyExistsError,
    EntityNotFoundError,
    InvalidAmountError,
    InvalidDateError,
    NoQualifyingAccountTypeError,
    PersonNotFoundError,
)
from src.logics.services import find_person
from src.logics.blue_rules import BlueAccountRules
from src.logics.green_rules import GreenAccountRules
from src.logics.red_rules import RedAccountRules
from src.logics.yellow_rules import YellowAccountRules
from src.models import AccountInfo, AccountType
from src.storage.storage import STORAGE_MANAGER
from src.utils import is_valid_date
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

ACCOUNT_RULES = {
    AccountType.BLUE: BlueAccountRules,
    AccountType.RED: RedAccountRules,
    AccountType.GREEN: GreenAccountRules,
    AccountType.YELLOW: YellowAccountRules,
}


class Logics:
    @staticmethod
    def _validate_amount(amount) -> int:
        """Returns the amount as a positive whole number, or raises.

        Rejects text, decimals, negatives and zero, so no caller has to guess
        whether the value it was handed is safe to do arithmetic with.
        """
        try:
            value = int(str(amount).strip())
        except (TypeError, ValueError):
            raise InvalidAmountError(f"'{amount}' is not a whole number") from None
        if value <= 0:
            raise InvalidAmountError("amount must be greater than zero")
        return value

    @staticmethod
    def _validate_date(date: str) -> str:
        """Returns the date unchanged if it is a real one, or raises.

        Sits beside _validate_amount so a subscription is checked in the one
        place that creates it, whichever caller asked for it.
        """
        if not is_valid_date(date):
            raise InvalidDateError(
                f"'{date}' is not a valid date, expected {SUBSCRIPTION_DATE_FORMAT}"
            )
        return date

    @classmethod
    def connect_user(cls, username: str) -> AccountInfo:
        try:
            return STORAGE_MANAGER.get_user_information(username)
        except EntityNotFoundError:
            logger.info("no account for username %s, attempting registration", username)
            return cls.register_user(username)

    @classmethod
    def get_balance(cls, user_info: AccountInfo) -> str:
        if user_info.locked:
            return "locked"

        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.get_balance(user_info)

    @classmethod
    def add_money(cls, user_info: AccountInfo, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = cls._validate_amount(amount)
        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.add_money(user_info, amount)

    @classmethod
    def get_money(cls, user_info: AccountInfo, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = cls._validate_amount(amount)
        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.get_money(user_info, amount)

    @classmethod
    def add_subscription(cls, user_info: AccountInfo, subscription_name: str, date: str, amount) -> str:
        if user_info.locked:
            return "locked"

        date = cls._validate_date(date)
        added = STORAGE_MANAGER.add_subscription(
            user_info.username, subscription_name, date, amount
        )
        if not added:
            return "subscription {} already exists".format(subscription_name)
        return "the subscription {} added successfully".format(subscription_name)

    @staticmethod
    def del_subscription(user_info: AccountInfo, subscription_name: str):
        if not STORAGE_MANAGER.delete_subscription(user_info.username, subscription_name):
            return "No subscription found matching {}.".format(subscription_name)
        return "the subscription {} deleted successfully".format(subscription_name)

    @classmethod
    def subscription_list(cls, user_info: AccountInfo):
        if user_info.account_type == AccountType.YELLOW:
            rules = ACCOUNT_RULES[user_info.account_type]
            return rules.subscription_list(user_info)  # TODO implement
        return STORAGE_MANAGER.get_subscriptions(user_info.username)

    @classmethod
    def register_user(cls, username: str) -> AccountInfo:
        """Opens an account for a person the personnel directory knows about.

        Each colour decides for itself who belongs to it, so this looks for
        the one that claims the person and then lets that colour run whatever
        onboarding it needs. Every way of not producing an account raises, so
        a caller that gets a return value got a real account and never has to
        check it for None.

        Raises:
            PersonNotFoundError: The directory has no record for this username.
            NoQualifyingAccountTypeError: The person meets no colour's criteria.
            AccountAlreadyExistsError: The username was taken in the meantime.
        """
        person = find_person(username)
        if person is None:
            raise PersonNotFoundError(
                f"'{username}' is not in the personnel directory"
            )

        match = next(
            ((account_type, rules)
             for account_type, rules in ACCOUNT_RULES.items()
             if rules.qualifies(person)),
            None,
        )
        if match is None:
            raise NoQualifyingAccountTypeError(
                f"'{username}' does not meet the criteria for any account type"
            )

        account_type, rules = match
        account = AccountInfo(
            username=username,
            balance=rules.INITIAL_BALANCE,
            account_type=account_type,
            locked=False,
        )
        if not STORAGE_MANAGER.add_account(account):
            raise AccountAlreadyExistsError(
                f"an account for '{username}' already exists"
            )

        rules.on_register(account, person)
        logger.info("registered %s as a %s account", username, account_type.name)
        return account

    @classmethod
    def del_account(cls, user_info: AccountInfo) -> tuple[bool, str]:
        """Closes an account and removes everything attached to it.

        The subscriptions go first. They live in a separate database, so no
        single transaction covers both, and the order decides what a failure
        leaves behind: stopping before the account is touched leaves the
        customer exactly as they were, whereas closing the account first and
        then failing would leave subscriptions with no owner - which the next
        registration of that username would inherit.

        Returns a (success, message) tuple so callers can branch on the
        boolean instead of inspecting the wording of the message.
        """
        removed = STORAGE_MANAGER.delete_subscriptions(user_info.username)
        deleted = STORAGE_MANAGER.delete_account(user_info.username)
        logger.info("account deletion for %s: %s, %d subscription(s) removed",
                    user_info.username, "done" if deleted else "no such account",
                    removed)
        if deleted:
            return True, f"Account '{user_info.username}' deleted successfully."
        return False, f"Account '{user_info.username}' not found."


    @classmethod
    def balance_next_day(cls, user_info: AccountInfo):
        """Project the account balance for the next billing day.

        If the subscription ends within the next month, no further charge is
        expected and the current balance stands. Otherwise the upcoming
        monthly amount is included and the account-type rules are applied.
        """
        subscription = cls.subscription_list(user_info)
        if not subscription:
            raise ValueError(f"no subscription for account {user_info.username}")

        _, end_date_raw, monthly_amount = subscription
        end_date = datetime.datetime.strptime(
            end_date_raw, SUBSCRIPTION_DATE_FORMAT
        ).date()

        if end_date <= datetime.date.today() + relativedelta(months=1):
            return user_info.balance

        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.balance_next_day(monthly_amount + user_info.balance)
        