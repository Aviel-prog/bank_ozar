from logics.base_rules import AccountRules


class BlueAccountRules(AccountRules):
    @staticmethod
    def get_money(user_info, amount: int) -> str:
        if amount > 100:
            return "you cant get more than 100"
        return AccountRules.get_money(user_info, amount)
