import datetime
import logging
from decimal import Decimal

from src.config import SUBSCRIPTION_DATE_FORMAT
from src.exceptions import EntityNotFoundError, InvalidAmountError
from src.logics.blue_rules import BlueAccountRules
from src.logics.green_rules import GreenAccountRules
from src.logics.red_rules import RedAccountRules
from src.logics.yellow_rules import YellowAccountRules
from src.models import AccountInfo, AccountType
from src.storage.storage import STORAGE_MANAGER
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

ACCOUNT_RULES = {
    AccountType.YELLOW: YellowAccountRules,
    AccountType.RED: RedAccountRules,
    AccountType.BLUE: BlueAccountRules,
    AccountType.GREEN: GreenAccountRules,
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

        amount = cls._validate_amount(amount)
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
        # people = get_people_list_from_web()
        # if people["serviceType"] == "קבע"
        #     if "3" in people["phone"] and "5" in people["phone"]:
        #         Logics.add_user_to_the_bank()
        #         Logics.save_changes()
        #     else:
        #         if "ן" in people["lastName"]:
        #             if people["department"] in ["אלנקטרוניקה", "פסיפס"]:
        #                 Logics.add_user_to_the_bank()
        #                 Logics.subscription_heandler()
        #                 Logics.save_changes()
        #     if people["rank"] == ["סמל", "סמר", "רבט"]:
        #         if "י" in people["firstName"]:
        #             Logics.add_user_to_the_bank()
        #             Logics.save_changes()
        #     if people["nickname"]:
        #         Logics.add_user_to_the_bank()
        #         Logics.subscription_heandler()
        #     if people["gender"] == "M" and "ת" in people["organization"]:
        #         Logics.add_user_to_the_bank()
        #         Logics.subscription_heandler()
        #         Logics.save_changes()
        pass

    @classmethod
    def del_account(cls, user_info: AccountInfo) -> tuple[bool, str]:
        """Deletes account using the provided user AccountInfo model.

        Returns a (success, message) tuple so callers can branch on the
        boolean instead of inspecting the wording of the message.
        """
        deleted = STORAGE_MANAGER.delete_account(user_info.username)
        logger.info("account deletion for %s: %s", user_info.username,
                    "done" if deleted else "no such account")
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
        