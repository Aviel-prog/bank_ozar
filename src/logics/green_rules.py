from src.logics.base_rules import AccountRules
from src.storage.storage import STORAGE_MANAGER


class GreenAccountRules(AccountRules):
    @staticmethod
    def get_balance(user_info) -> str:
        user_info.balance += 2
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return AccountRules.get_balance(user_info)

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        if amount % 2 != 0:
            amount -= 100
        return AccountRules.balance_next_pay_day(amount)
