from constants import AccountType
from logics.base_rules import AccountRules
from models import AccountInfo
from storage.storage import STORAGE_MANAGER


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

    @staticmethod
    def subscription_list(user_info: AccountInfo):
        if user_info.username == AccountType.YELLOW:  # TODO check it
            return False
        return STORAGE_MANAGER.show_subscriptions(user_info.username)

    @staticmethod
    def balance_next_day(amount: int):
        if amount > 0:
            return "less than 0 so lock next pay day"  # TODO understand it
        else:
            return "next pay day you have X"
