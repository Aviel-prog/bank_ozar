import datetime

from constants import AccountType, DB_PATH
from models import AccountInfo
from storage import STORAGE_MANAGER


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

        if user_info.account_type == AccountType.GREEN:
            user_info.balance += 2
            STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        elif user_info.account_type == AccountType.YELLOW:
            return "X in your bank"
        return "{balance} in your bank".format(balance=user_info.balance)

    @classmethod
    def add_money(cls, user_info: AccountInfo, amount):
        if user_info.locked:
            return "locked"

        amount = int(amount)
        if amount < 0:
            return "cant Zero money"

        if user_info.account_type == AccountType.RED:
            if datetime.date.today().day % 2 != 0 and amount > 300:
                return "no more than 300 on odd day"

        user_info.balance += amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "added successfully"

    @classmethod
    def get_money(cls, user_info: AccountInfo, amount: int):
        if user_info.locked:
            return "locked"

        if user_info.account_type == AccountType.BLUE:
            if amount > 100:
                return "you cant get more than 100"

        if user_info.account_type == AccountType.YELLOW:
            if user_info.balance - amount < 0:
                user_info.balance -= amount
                STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
                STORAGE_MANAGER.update_lock(user_info.username, True)
                return "you have less than 0 in your account now"
            else:  # TODO delete not relevant
                user_info.balance -= amount
                StorageManager.update_balance(user_info.username, user_info.balance)
                return "got the money successfully"

        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "got the money successfully"

    def add_subscription(self):
        pass

    def delete_subscription(self, user_info: AccountInfo, subscription_name: str):
        pass

    def list_subscription(self):
        pass

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
    def del_account(cls, user_info: AccountInfo) -> str:
        """Deletes account using the provided user AccountInfo model."""
        deleted = STORAGE_MANAGER.delete_account(user_info.username, DB_PATH)
        if deleted:
            return f"Account '{user_info.username}' deleted successfully."
        return f"Account '{user_info.username}' not found.

#
# import datetime
# from abc import ABC, abstractmethod
#
# from constants import AccountType, DB_PATH
# from models import AccountInfo
# from storage import StorageManager
#
#
# class BaseLogics(ABC):
#     """Abstract Base Class providing common logic and defining account interfaces."""
#
#     @classmethod
#     def connect_user(cls, username: str) -> AccountInfo:
#         connection = StorageManager()
#         if connection.is_user_exist(username):
#             return connection.get_user_information(username)
#         print("user not exist")
#         return cls.register_user(username)
#
#     @classmethod
#     def get_balance(cls, user_info: AccountInfo) -> str:
#         if user_info.locked:
#             return "locked"
#         return f"{user_info.balance} in your bank"
#
#     @classmethod
#     def add_money(cls, user_info: AccountInfo, amount: int) -> str:
#         if user_info.locked:
#             return "locked"
#
#         amount = int(amount)
#         if amount <= 0:
#             return "cant Zero money"
#
#         user_info.balance += amount
#         StorageManager.update_balance(user_info.username, user_info.balance)
#         return "added successfully"
#
#     @classmethod
#     def get_money(cls, user_info: AccountInfo, amount: int) -> str:
#         if user_info.locked:
#             return "locked"
#
#         if user_info.balance - amount < 0:
#             return "insufficient funds"
#
#         user_info.balance -= amount
#         StorageManager.update_balance(user_info.username, user_info.balance)
#         return "got the money successfully"
#
#     @classmethod
#     def register_user(cls, username: str) -> AccountInfo:
#         pass
#
#     @classmethod
#     def del_account(cls, user_info: AccountInfo) -> str:
#         """Deletes account using the provided user AccountInfo model."""
#         deleted = StorageManager.delete_account(user_info.username, DB_PATH)
#         if deleted:
#             return f"Account '{user_info.username}' deleted successfully."
#         return f"Account '{user_info.username}' not found."
#
#
# # ==========================================
# # 1. GREEN Account Logic (Bonus on balance check)
# # ==========================================
# class GreenAccountLogics(BaseLogics):
#     @classmethod
#     def get_balance(cls, user_info: AccountInfo) -> str:
#         if user_info.locked:
#             return "locked"
#
#         user_info.balance += 2
#         StorageManager.update_balance(user_info.username, user_info.balance)
#         return f"{user_info.balance} in your bank"
#
#
# # ==========================================
# # 2. YELLOW Account Logic (Masked balance & Overdraft lock)
# # ==========================================
# class YellowAccountLogics(BaseLogics):
#     @classmethod
#     def get_balance(cls, user_info: AccountInfo) -> str:
#         if user_info.locked:
#             return "locked"
#         return "X in your bank"
#
#     @classmethod
#     def get_money(cls, user_info: AccountInfo, amount: int) -> str:
#         if user_info.locked:
#             return "locked"
#
#         user_info.balance -= amount
#         StorageManager.update_balance(user_info.username, user_info.balance)
#
#         if user_info.balance < 0:
#             StorageManager.update_lock(user_info.username, True)
#             user_info.locked = True
#             return "you have less than 0 in your account now"
#
#         return "got the money successfully"
#
#
# # ==========================================
# # 3. RED Account Logic (Odd day deposit limits)
# # ==========================================
# class RedAccountLogics(BaseLogics):
#     @classmethod
#     def add_money(cls, user_info: AccountInfo, amount: int) -> str:
#         if user_info.locked:
#             return "locked"
#
#         amount = int(amount)
#         if amount <= 0:
#             return "cant Zero money"
#
#         if datetime.date.today().day % 2 != 0 and amount > 300:
#             return "no more than 300 on odd day"
#
#         return super().add_money(user_info, amount)
#
#
# # ==========================================
# # 4. BLUE Account Logic (Withdrawal capped at 100)
# # ==========================================
# class BlueAccountLogics(BaseLogics):
#     @classmethod
#     def get_money(cls, user_info: AccountInfo, amount: int) -> str:
#         if user_info.locked:
#             return "locked"
#
#         if amount > 100:
#             return "you cant get more than 100"
#
#         return super().get_money(user_info, amount)
#
#
# # ==========================================
# # Factory Helper (Dispatches correct class)
# # ==========================================
# class LogicsFactory:
#     """Routes AccountInfo to the corresponding specialized logic class."""
#
#     _LOGIC_MAP = {
#         AccountType.GREEN: GreenAccountLogics,
#         AccountType.YELLOW: YellowAccountLogics,
#         AccountType.RED: RedAccountLogics,
#         AccountType.BLUE: BlueAccountLogics,
#     }
#
#     @classmethod
#     def get_logic_handler(cls, account_type: AccountType) -> type[BaseLogics]:
#         return cls._LOGIC_MAP.get(account_type, BaseLogics)
