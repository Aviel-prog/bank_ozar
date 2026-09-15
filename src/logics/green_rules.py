import logging

from src.logics.base_rules import AccountRules
from src.storage.storage import STORAGE_MANAGER

logger = logging.getLogger(__name__)

QUALIFYING_RANKS = ("סמל", "סמר", "רבט")


class GreenAccountRules(AccountRules):
    @staticmethod
    def qualifies(person: dict) -> bool:
        return person["rank"] in QUALIFYING_RANKS and "י" in person["firstName"]

    @staticmethod
    def get_balance(user_info) -> str:
        user_info.balance += 2
        STORAGE_MANAGER.update_balance(user_info.username, user_info.balance)
        logger.info("green bonus of 2 credited to %s, balance now %s",
                    user_info.username, user_info.balance)
        return AccountRules.get_balance(user_info)

    @staticmethod
    def balance_next_pay_day(amount: int) -> str:
        if amount % 2 != 0:
            amount -= 100
        return AccountRules.balance_next_pay_day(amount)
