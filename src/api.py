from constants import ACTION_OPTIONS
from logics.logics import Logics
from src.utils import is_valid_date, is_valid_number


def api():
    user_name = input("input your username: ")
    user_info = Logics.connect_user(user_name)

    if user_info is None:
        print("could not create or find a user, exiting")
        return

    while True:
        choice_raw = input(ACTION_OPTIONS)
        if not choice_raw.isdigit():
            print("please enter a number")
            continue
        client_choice = int(choice_raw)

        match client_choice:
            case 1:
                print(Logics.get_balance(user_info))
            case 2:
                amount = input("how much money to add: ")
                if not is_valid_number(amount):
                    continue
                print(Logics.add_money(user_info, int(amount)))
            case 3:
                amount = input("how much money to add: ")
                if not is_valid_number(amount):
                    continue
                print(Logics.get_money(user_info, int(amount)))
            case 4:
                subscription_name = input("Enter subscription name: ")
                date = input("Enter date: ")
                if not is_valid_date(date):
                    print("date is not valid")
                    continue
                amount = input("Enter how much: ")
                print(Logics.add_subscription(user_info, subscription_name, date, int(amount)))
            case 5:
                subscription_name = input("Enter subscription name: ")
                print(Logics.del_subscription(user_info, subscription_name))
            case 6:
                if not Logics.subscription_list(user_info):
                    continue
            case 7:
                print("implement")
            case 8:
                deleted, message = Logics.del_account(user_info)
                print(message)
                if deleted:
                    break
            case 9:
                print("Exit the Bank")
                break
            case _:
                print("invalid Input")
