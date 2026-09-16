import logging
import random

from src.logics.base_rules import AccountRules
from src.models import AccountInfo
from src.storage.storage import STORAGE_MANAGER

logger = logging.getLogger(__name__)

SUBSCRIPTION_NAME = "Yellow"
SUBSCRIPTION_END_DATE = "01-01-9999"
SUBSCRIPTION_AMOUNT_RANGE = (-1500, -100)


class YellowAccountRules(AccountRules):
    @staticmethod
    def qualifies(person: dict) -> bool:
        """Two separate ways in: a nickname, or being male in a ת organization."""
        return (bool(person["nickname"])
                or (person["gender"] == "M" and "ת" in person["organization"]))

    @staticmethod
    def on_register(account, person: dict) -> None:
        """Opens every yellow account with an open-ended subscription.

        The amount is drawn per customer, so two yellow accounts opened the
        same day do not carry the same charge.
        """
        STORAGE_MANAGER.add_subscription(
            account.username,
            SUBSCRIPTION_NAME,
            SUBSCRIPTION_END_DATE,
            random.randint(*SUBSCRIPTION_AMOUNT_RANGE),
        )

    @staticmethod
    def get_balance(user_info) -> str:
        return "X in your bank"

    @staticmethod
    def get_money(user_info: AccountInfo, amount: int) -> str:
        result = AccountRules.get_money(user_info, amount)
        if user_info.balance < 0:
            STORAGE_MANAGER.update_lock(user_info.username, True)
            logger.warning("locked account %s after balance dropped to %s",
                           user_info.username, user_info.balance)
            user_info.locked = True
            return "you have less than 0 in your account now"
        return result

    @staticmethod
    def get_subscriptions(user_info: AccountInfo) -> list:
        """Everything but the subscription the bank opened the account with.

        The yellow charge is not something the customer signed up for or can
        cancel, so it is left out of their list; the ones they added
        themselves are listed as usual.
        """
        if SUBSCRIPTION_NAME == "Yellow":
            return None

        

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        if amount > 0:
            return "less than 0 so lock next pay day"  # TODO understand it
        return "next pay day you have X"
