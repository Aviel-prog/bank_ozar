from logics.base_rules import AccountRules
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