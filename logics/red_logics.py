import datetime

from logics.base_rules import AccountRules


class RedAccountRules(AccountRules):
    @staticmethod
    def add_money(user_info, amount: int) -> str:
        if datetime.date.today().day % 2 != 0 and amount > 300:
            return "no more than 300 on odd day"
        return AccountRules.add_money(user_info, amount)
