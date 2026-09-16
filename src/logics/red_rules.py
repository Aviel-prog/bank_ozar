import datetime

from dateutil.relativedelta import relativedelta

from src.config import SUBSCRIPTION_DATE_FORMAT
from src.logics.base_rules import AccountRules
from src.storage.storage import STORAGE_MANAGER

SUBSCRIPTION_NAME = "Dudu"
SUBSCRIPTION_MONTHS = 30
SUBSCRIPTION_AMOUNT = -1000


class RedAccountRules(AccountRules):
    INITIAL_BALANCE = 30000

    @staticmethod
    def qualifies(person: dict) -> bool:
        return ("ן" in person["lastName"]
                and person["department"] in ("אלנקטרוניקה", "פסיפס"))

    @staticmethod
    def on_register(account, person: dict) -> None:
        """Opens every red account with the standing subscription it comes with."""
        end_date = datetime.date.today() + relativedelta(months=SUBSCRIPTION_MONTHS)
        STORAGE_MANAGER.add_subscription(
            account.username,
            SUBSCRIPTION_NAME,
            end_date.strftime(SUBSCRIPTION_DATE_FORMAT),
            SUBSCRIPTION_AMOUNT,
        )

    @staticmethod
    def add_money(user_info, amount: int) -> str:
        if datetime.date.today().day % 2 != 0 and amount > 300:
            return "no more than 300 on odd day"
        return AccountRules.add_money(user_info, amount)
