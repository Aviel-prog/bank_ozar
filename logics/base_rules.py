from storage.storage import STORAGE_MANAGER


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
