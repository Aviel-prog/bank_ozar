from constants import ACTION_OPTIONS
from logics import Logics
from storage import init_database
from utils import is_valid_menu_choice


def api():
    user_name = input("input your username: ")
    user_info = Logics.connect_user(user_name)

    if user_info is None:
        print("could not create or find a user, exiting")
        return

    while True:
        choice_raw = input(ACTION_OPTIONS)
        if not is_valid_menu_choice(choice_raw):
            print("please enter a number")
            continue
        client_choice = int(choice_raw)

        match client_choice:
            case 1:
                print(Logics.get_balance(user_info))
            case 2:
                amount = input("how much money to add: ")
                print(Logics.add_money(user_info, amount))
            case 3:
                amount = input("how much money to get: ")
                print(Logics.get_money(user_info, amount))
            case 4:
                print("add subscription - not implemented yet")
            case 5:
                subscription_name = input("Enter subscription name: ")
                Logics.delete_subscription(user_info, subscription_name)
                print("delete subscription - not implemented yet")
            case 6:
                print("list subscriptions - not implemented yet")
            case 7:
                print(Logics.delete_account(user_info))
            case 8:
                print("Exit the Bank")
                break
            case _:
                print("invalid Input")


def main():
    init_database()
    api()


if __name__ == "__main__":
    main()
