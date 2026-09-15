from constants import AccountType
from logics.blue_logics import BlueAccountRules
from logics.green_logics import GreenAccountRules
from logics.red_logics import RedAccountRules
from logics.yellow_logics import YellowAccountRules
from models import AccountInfo
from storage.storage import STORAGE_MANAGER

ACCOUNT_RULES = {
    AccountType.YELLOW: YellowAccountRules(),
    AccountType.RED: RedAccountRules(),
    AccountType.BLUE: BlueAccountRules(),
    AccountType.GREEN: GreenAccountRules(),
}


class Logics:
    @classmethod
    def connect_user(cls, username: str) -> AccountInfo:
        if STORAGE_MANAGER.is_user_exist(username):
            return STORAGE_MANAGER.get_user_information(username)
        print("user not exist")
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

        amount = int(amount)
        if amount < 0:
            return "cant Zero money"

        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.add_money(user_info, amount)

    @classmethod
    def get_money(cls, user_info: AccountInfo, amount) -> str:
        if user_info.locked:
            return "locked"

        amount = int(amount)

        rules = ACCOUNT_RULES[user_info.account_type]
        return rules.get_money(user_info, amount)

    def add_subscription(self, user_info: AccountInfo, subscription_name: str, date: str, amount: int):
        if user_info.locked:
            return "locked"
        return STORAGE_MANAGER.add_subscription(user_info.username, subscription_name, date, amount)

    @staticmethod
    def del_subscription(user_info: AccountInfo, subscription_name: str):
        if STORAGE_MANAGER.delete_subscription(user_info.username, subscription_name):
            return "the subscription {} deleted successfully".format(subscription_name)

    @staticmethod
    def subscription_list(user_info: AccountInfo):
        if user_info.account_type == AccountType.YELLOW:
            rules = ACCOUNT_RULES[user_info.account_type]
            return rules.subscription_list(user_info)  # TODO implement
        return STORAGE_MANAGER.show_all_subscriptions(user_info.username)

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
        if deleted:
            return True, f"Account '{user_info.username}' deleted successfully."
        return False, f"Account '{user_info.username}' not found."
