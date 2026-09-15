from storage.storage import STORAGE_MANAGER


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
    def _withdraw(user_info, amount: int) -> str:
        """Takes the money out and saves it, with no limit of any kind.

        Account types that are allowed to overdraw call this directly instead
        of ``get_money``, so the unlimited path is written once.
        """
        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        return "got the money successfully"

    @staticmethod
    def get_money(user_info, amount: int) -> str:
        """Withdraws, then locks the account if it dropped below zero.

        This is the cautious default, so an account type that says nothing
        about withdrawals is protected rather than free to overdraw. Types
        that should be unlimited opt out by overriding this method.

        The lock is written to the database and mirrored onto ``user_info``.
        Without the second write the object the session keeps using would
        still report itself unlocked, and every later check would wave the
        customer through until they reconnected.
        """
        result = AccountRules._withdraw(user_info, amount)
        if user_info.balance < 0:
            STORAGE_MANAGER.update_lock(user_info.username, True)
            user_info.locked = True
            return "you have less than 0 in your account now"
        return result

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        return "next pay day you will have X"
