from src.models import AccountType
from src.logics.base_rules import AccountRules
from src.models import AccountInfo
from src.storage.storage import STORAGE_MANAGER


class YellowAccountRules(AccountRules):
    @staticmethod
    def get_balance(user_info) -> str:
        return "X in your bank"

    @staticmethod
    def get_money(user_info, amount: int) -> str:
        result = AccountRules.get_money(user_info, amount)
        if user_info.balance < 0:
            STORAGE_MANAGER.update_lock(user_info.username, True)
            return "you have less than 0 in your account now"
        return result

    @staticmethod
    def subscription_list(user_info: AccountInfo):
        if user_info.username == AccountType.YELLOW:  # TODO check it
            return False
        return STORAGE_MANAGER.show_subscriptions(user_info.username)

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        if amount > 0:
            return "less than 0 so lock next pay day"  # TODO understand it
        return "next pay day you have X"
