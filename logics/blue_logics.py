from logics.base_rules import AccountRules


class BlueAccountRules(AccountRules):
    def get_money(self, user_info, amount: int) -> str:
        if amount > 100:
            return "you cant get more than 100"
        return super().get_money(user_info, amount)