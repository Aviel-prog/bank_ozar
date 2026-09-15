import logging

from src.storage.storage import STORAGE_MANAGER

logger = logging.getLogger(__name__)


class AccountRules:
    """Default behaviour shared by every account type.

    The rules carry no state, so every method is a staticmethod and the
    class itself is used directly - no instance is ever created. Subclasses
    that want the default behaviour call it through ``AccountRules.<method>``
    rather than ``super()``, which is unavailable without a bound instance.
    """

    #: What a newly opened account of this colour starts with.
    INITIAL_BALANCE = 0

    @staticmethod
    def qualifies(person: dict) -> bool:
        """Whether this person should be opened as this kind of account.

        The criteria across the colours do not overlap - a person qualifies
        for exactly one - so whichever class says yes is the answer. The base
        says no, so a colour that defines no criteria is never handed anyone.
        """
        return False

    @staticmethod
    def on_register(account, person: dict) -> None:
        """Extra steps to run once, when this kind of account is opened.

        Doing nothing is the default, so a colour only mentions onboarding if
        it actually has some.
        """

    @staticmethod
    def get_balance(user_info) -> str:
        return "{balance} in your bank".format(balance=user_info.balance)

    @staticmethod
    def add_money(user_info, amount: int) -> str:
        user_info.balance += amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        logger.info("deposit of %s by %s, balance now %s",
                    amount, user_info.username, user_info.balance)
        return "added successfully"

    @staticmethod
    def get_money(user_info, amount: int) -> str:
        user_info.balance -= amount
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        logger.info("withdrawal of %s by %s, balance now %s",
                    amount, user_info.username, user_info.balance)
        return "got the money successfully"

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        return "next pay day you will have X"
