"""Domain models for the banking application."""

from enum import Enum


class AccountType(Enum):
    """The account tiers, each with its own rule set."""

    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


class AccountInfo:
    """Represents a customer's bank account data and status."""
    def __init__(self, username: str, balance: int, account_type: AccountType, locked: bool):
        """Initializes an AccountInfo instance with customer parameters.

        Args:
            username (str): Unique account holder name.
            balance (int): Initial account balance.
            account_type (AccountType): Account classification.
            locked (bool): Account lock status.
        """
        self.username = username
        self.balance = balance
        self.account_type = account_type
        self.locked = locked

    def __repr__(self) -> str:
        """Returns a human-readable representation of the AccountInfo object."""
        return (
            f"AccountInfo(username='{self.username}', balance={self.balance}, "
            f"account_type={self.account_type}, locked={self.locked})"
        )