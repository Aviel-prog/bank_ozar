from logics.base_rules import AccountRules


class BlueAccountRules(AccountRules):
    @staticmethod
    def get_money(user_info, amount: int) -> str:
        """Caps a single withdrawal at 100, but allows any overdraft under it."""
        if amount > 100:
            return "you cant get more than 100"
        return AccountRules._withdraw(user_info, amount)
