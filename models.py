from constants import AccountType


class AccountInfo:
    def __init__(self, username, balance, account_type: AccountType, locked):
        self.username = username
        self.balance = balance
        self.account_type = account_type
        self.locked = locked
