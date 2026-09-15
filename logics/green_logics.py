from logics.base_rules import AccountRules
from storage.storage import STORAGE_MANAGER


class GreenAccountRules(AccountRules):
    def get_balance(self, user_info) -> str:
        user_info.balance += 2
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "{balance} in your bank".format(balance=user_info.balance)
