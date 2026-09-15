from constants import AccountType
from logics.base_rules import AccountRules
from models import AccountInfo
from storage.storage import STORAGE_MANAGER


class YellowAccountRules(AccountRules):
    @staticmethod
    def get_balance(user_info) -> str:
        return "X in your bank"

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
