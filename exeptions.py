"""Database exceptions for the banking application."""


class BankAppError(Exception):
    """Base exception for banking application domain errors."""


class EntityNotFoundError(BankAppError):
    """Raised when a requested database record is not found."""


class InsufficientFundsError(BankAppError):
    """Raised when an operation exceeds account overdraft boundaries."""


class LimitExceededError(BankAppError):
    """Raised when a single or daily transaction threshold is breached."""


class DatabaseError(BankAppError):
    """Raised when an unexpected SQLite error occurs."""