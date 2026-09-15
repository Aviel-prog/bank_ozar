import datetime

from constants import AccountType
from storage import STORAGE_MANAGER


class AccountRules:
    """Default behaviour shared by every account type."""

    def get_balance(self, user_info) -> str:
        return "{balance} in your bank".format(balance=user_info.balance)

    def add_money(self, user_info, amount: int) -> str:
        user_info.balance += amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "added successfully"

    def get_money(self, user_info, amount: int) -> str:
        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "got the money successfully"


class RedAccountRules(AccountRules):
    def add_money(self, user_info, amount: int) -> str:
        if datetime.date.today().day % 2 != 0 and amount > 300:
            return "no more than 300 on odd day"
        return super().add_money(user_info, amount)


class BlueAccountRules(AccountRules):
    def get_money(self, user_info, amount: int) -> str:
        if amount > 100:
            return "you cant get more than 100"
        return super().get_money(user_info, amount)


class YellowAccountRules(AccountRules):
    def get_balance(self, user_info) -> str:
        return "X in your bank"

    def get_money(self, user_info, amount: int) -> str:
        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        if user_info.balance < 0:
            STORAGE_MANAGER.update_lock(user_info.username, True)
            return "you have less than 0 in your account now"
        return "got the money successfully"


class GreenAccountRules(AccountRules):
    def get_balance(self, user_info) -> str:
        user_info.balance += 2
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "{balance} in your bank".format(balance=user_info.balance)


ACCOUNT_RULES = {
    AccountType.YELLOW: YellowAccountRules(),
    AccountType.RED: RedAccountRules(),
    AccountType.BLUE: BlueAccountRules(),
    AccountType.GREEN: GreenAccountRules(),
}