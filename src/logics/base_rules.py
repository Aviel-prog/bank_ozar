from src.storage.storage import STORAGE_MANAGER


class AccountRules:
    """Default behaviour shared by every account type.

    The rules carry no state, so every method is a staticmethod and the
    class itself is used directly - no instance is ever created. Subclasses
    that want the default behaviour call it through ``AccountRules.<method>``
    rather than ``super()``, which is unavailable without a bound instance.
    """

    @staticmethod
    def get_balance(user_info) -> str:
        return "{balance} in your bank".format(balance=user_info.balance)

    @staticmethod
    def add_money(user_info, amount: int) -> str:
        user_info.balance += amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "added successfully"

    @staticmethod
    def get_money(user_info, amount: int) -> str:
        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "got the money successfully"

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        return "next pay day you will have X"
