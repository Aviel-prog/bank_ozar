"""Database exceptions for the banking application."""


class BankAppError(Exception):
    """Base exception for banking application domain errors."""


class EntityNotFoundError(BankAppError):
    """Raised when a requested database record is not found."""


class PersonNotFoundError(BankAppError):
    """Raised when the personnel directory holds no record for a username.

    Distinct from EntityNotFoundError, which is about the bank's own tables -
    this one means the person is unknown to the organisation entirely, so no
    account could be opened for them under any rule.
    """


class InsufficientFundsError(BankAppError):
    """Raised when an operation exceeds account overdraft boundaries."""


class LimitExceededError(BankAppError):
    """Raised when a single or daily transaction threshold is breached."""


class DatabaseError(BankAppError):
    """Raised when an unexpected SQLite error occurs."""


class InvalidAmountError(BankAppError):
    """Raised when a transaction amount is not a positive whole number."""
