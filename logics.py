import datetime

from constants import AccountType
from models import AccountInfo
from storage import StorageManager


class Logics:
    @classmethod
    def connect_user(cls, username: str) -> AccountInfo:
        connection = StorageManager()
        if connection.is_user_exist(username):
            return connection.get_user_information(username)
        print("user not exist")
        return cls.register_user(username)

    @classmethod
    def get_balance(cls, user_info: AccountInfo) -> str:
        if user_info.locked:
            return "locked"

        if user_info.account_type == AccountType.GREEN:
            user_info.balance += 2
            StorageManager.update_balance(user_info.username, user_info.balance)
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
        StorageManager.update_balance(user_info.username, user_info.balance)
        return "added successfully"

    @classmethod
    def get_money(cls, user_info: AccountInfo, amount):
        if user_info.locked:
            return "locked"

        amount = int(amount)

        if user_info.account_type == AccountType.BLUE:
            if amount > 100:
                return "you cant get more than 100"

        if user_info.account_type == AccountType.YELLOW:
            if user_info.balance - amount < 0:
                user_info.balance -= amount
                StorageManager.update_balance(user_info.username, user_info.balance)
                StorageManager.update_lock(user_info.username, True)
                return "you have less than 0 in your account now"
            else:  # TODO delete not relevant
                user_info.balance -= amount
                StorageManager.update_balance(user_info.username, user_info.balance)
                return "got the money successfully"

        user_info.balance -= amount
        StorageManager.update_balance(user_info.username, user_info.balance)
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
    def delete_account(cls, user_info: AccountInfo):
        pass
