action_options = ("1. balance\n",
                  "2. add money\n",
                  "3. pull money\n",
                  "4. subscription action"
                  "5. delete account\n"
                  "6. exit the app"
                  )


# ---------------- DB  -----------------------

class StorageManager:
    def __init__(self):
        self.connect()

    def connect(self):
        pass

    def close(self):
        pass

    def is_user_exist(self):
        pass

    def get_user_information(self, user_name):
        pass

    def get_account_type(self):
        pass

    def load_db(self, param):
        pass


# ---------------- Logic -----------------------
class Logics:
    def __init__(self):
        pass

    @staticmethod
    def handler_user(self, user_name):
        result = StorageManager.is_user_exist(user_name)
        if not result:
            add_user(user_name)
        return True
    def add_user_to_the_bank(self):
        pass
    def show_balance(self):
        pass

    def add_money(self):
        pass

    def get_money(self):
        pass

    def delete_account(self):
        pass

    def subscription_heandler(self):
        pass
    def save_changes(self):
        pass
# ---------------- Add user  -----------------------


def get_people_list_from_web():
    pass


def add_user(username):
    pass
    # people = get_people_list_from_web()
    # if people["serviceType"] == "קבע"
    #     if "3" in people["phone"] and "5" in people["phone"]:
    #         Logics.add_user_to_the_bank()
    #         Logics.save_changes()
    #     else:
    #         if "ן" in people["lastName"]:
    #             if people["department"] in ["אלנקטרוניקה", "פסיפס"]:
    #                 Logics.add_user_to_the_bank()
    #                 Logics.subscription_heandler()
    #                 Logics.save_changes()
    #     if people["rank"] == ["סמל", "סמר", "רבט"]:
    #         if "י" in people["firstName"]:
    #             Logics.add_user_to_the_bank()
    #             Logics.save_changes()
    #     if people["nickname"]:
    #         Logics.add_user_to_the_bank()
    #         Logics.subscription_heandler()
    #     if people["gender"] == "M" and "ת" in people["organization"]:
    #         Logics.add_user_to_the_bank()
    #         Logics.subscription_heandler()
    #         Logics.save_changes()


# -------------------------------------------------------- # main


def api():
    user_name = input("input your username: ")
    Logics.handler_user(user_name)
    client_choice = None
    while client_choice == "exit":
        client_choice = int(input(action_options))
        match client_choice:
            case 1:
                print("balance")
                Logics.show_balance()
            case 2:
                print("add money")
                Logics.add_money()
            case 3:
                print("get money")
                Logics.get_money()
            case 4:
                client_choice = int(input("which subscription action you want to do "))
                print("subscriptions - 3 options")
                Logics.subscription_heandler()
            case 5:
                print("delete account")
                Logics.delete_account()
            case 6:
                print("Exit the Bank")
            case _:
                pass


def main():
    StorageManager()
    api()


if __name__ == "__main__":
    main()
