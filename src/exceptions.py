"""Database exceptions for the banking application."""


class BankAppError(Exception):
    """Base exception for banking application domain errors."""


class EntityNotFoundError(BankAppError):
    """Raised when a requested database record is not found."""


class RegistrationError(BankAppError):
    """Base for every reason an account could not be opened.

    Registration either produces an account or explains itself, so callers can
    catch this one class and still print something the customer can act on.
    """


class PersonNotFoundError(RegistrationError):
    """Raised when the personnel directory holds no record for a username.

    Distinct from EntityNotFoundError, which is about the bank's own tables -
    this one means the person is unknown to the organisation entirely, so no
    account could be opened for them under any rule.
    """


class NoQualifyingAccountTypeError(RegistrationError):
    """Raised when a person is in the directory but meets no colour's criteria."""


class AccountAlreadyExistsError(RegistrationError):
    """Raised when the username is taken at the moment of opening the account.

    Registration only runs after a lookup found nobody, so a clash here means
    the account appeared in between - not an ordinary outcome.
    """


class InsufficientFundsError(BankAppError):
    """Raised when an operation exceeds account overdraft boundaries."""


class LimitExceededError(BankAppError):
    """Raised when a single or daily transaction threshold is breached."""


class DatabaseError(BankAppError):
    """Raised when an unexpected SQLite error occurs."""


class InvalidAmountError(BankAppError):
    """Raised when a transaction amount is not a positive whole number."""
