import datetime

from constants import AccountType
from exeptions import EntityNotFoundError, InvalidAmountError
from logics.blue_logics import BlueAccountRules
from logics.green_logics import GreenAccountRules
from logics.red_logics import RedAccountRules
from logics.yellow_logics import YellowAccountRules
from models import AccountInfo
from storage.storage import StorageManager
from dateutil.relativedelta import relativedelta

ACCOUNT_RULES = {
    AccountType.YELLOW: YellowAccountRules,
    AccountType.RED: RedAccountRules,
    AccountType.BLUE: BlueAccountRules,
    AccountType.GREEN: GreenAccountRules,
}

SUBSCRIPTION_DATE_FORMAT = "%d-%m-%Y"


class Logics:
    def __init__(self, storage: StorageManager):
        """Holds the storage the bank operations run against.

        Taking the manager as a parameter instead of reaching for a module
        level singleton lets a test hand in a stand-in storage and keeps the
        class from deciding on its own which database it talks to.

        Args:
            storage (StorageManager): Storage used for every account and
                subscription operation.
        """
        self.storage = storage

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

    def connect_user(self, username: str) -> AccountInfo:
        try:
            return self.storage.get_user_information(username)
        except EntityNotFoundError:
            print("user not exist")
            return self.register_user(username)

    def get_balance(self, user_info: AccountInfo) -> str:
        if user_info.locked:
            return "locked"

        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.get_balance(user_info)

    def add_money(self, user_info: AccountInfo, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = self._validate_amount(amount)
        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.add_money(user_info, amount)

    def get_money(self, user_info: AccountInfo, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = self._validate_amount(amount)
        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.get_money(user_info, amount)

    def add_subscription(self, user_info: AccountInfo, subscription_name: str, date: str, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = self._validate_amount(amount)
        added = self.storage.add_subscription(
            user_info.username, subscription_name, date, amount
        )
        if not added:
            return "subscription {} already exists".format(subscription_name)
        return "the subscription {} added successfully".format(subscription_name)

    def del_subscription(self, user_info: AccountInfo, subscription_name: str):
        if not self.storage.delete_subscription(user_info.username, subscription_name):
            return "No subscription found matching {}.".format(subscription_name)
        return "the subscription {} deleted successfully".format(subscription_name)

    def subscription_list(self, user_info: AccountInfo):
        if user_info.account_type == AccountType.YELLOW:
            rules = ACCOUNT_RULES[user_info.account_type]
            return rules.subscription_list(user_info)  # TODO implement
        return self.storage.show_subscriptions(user_info.username)

    def register_user(self, username: str) -> AccountInfo:
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

    def del_account(self, user_info: AccountInfo) -> tuple[bool, str]:
        """Deletes account using the provided user AccountInfo model.

        Returns a (success, message) tuple so callers can branch on the
        boolean instead of inspecting the wording of the message.
        """
        deleted = self.storage.delete_account(user_info.username)
        if deleted:
            return True, f"Account '{user_info.username}' deleted successfully."
        return False, f"Account '{user_info.username}' not found."

    def balance_next_day(self, user_info: AccountInfo):
        """Project the account balance for the next billing day.

        If the subscription ends within the next month, no further charge is
        expected and the current balance stands. Otherwise the upcoming
        monthly amount is included and the account-type rules are applied.
        """
        subscription = self.subscription_list(user_info)
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
