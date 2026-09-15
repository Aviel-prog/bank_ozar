from src.logics.base_rules import AccountRules


class BlueAccountRules(AccountRules):
    INITIAL_BALANCE = 1700

    @staticmethod
    def qualifies(person: dict) -> bool:
        return (person["serviceType"] == "קבע"
                and "3" in person["phone"]
                and "5" in person["phone"])

    @staticmethod
    def get_money(user_info, amount: int) -> str:
        if amount > 100:
            return "you cant get more than 100"
        return AccountRules.get_money(user_info, amount)
