from src.exceptions import BankAppError
from src.logics.logics import Logics
from src.menu import MENU_OPTIONS, render_menu
from src.models import AccountInfo
from src.utils import is_valid_date


def _balance(user_info: AccountInfo) -> bool:
    print(Logics.get_balance(user_info))
    return True


def _deposit(user_info: AccountInfo) -> bool:
    amount = input("how much money to add: ")
    print(Logics.add_money(user_info, amount))
    return True


def _withdraw(user_info: AccountInfo) -> bool:
    amount = input("how much money to get: ")
    print(Logics.get_money(user_info, amount))
    return True


def _add_subscription(user_info: AccountInfo) -> bool:
    subscription_name = input("Enter subscription name: ")
    date = input("Enter date: ")
    if not is_valid_date(date):
        print("date is not valid")
        return True
    amount = input("Enter how much: ")
    print(Logics.add_subscription(user_info, subscription_name, date, amount))
    return True


def _remove_subscription(user_info: AccountInfo) -> bool:
    subscription_name = input("Enter subscription name: ")
    print(Logics.del_subscription(user_info, subscription_name))
    return True


def _list_subscriptions(user_info: AccountInfo) -> bool:
    Logics.subscription_list(user_info)
    return True


def _balance_next_day(user_info: AccountInfo) -> bool:
    print("implement")
    return True


def _purge(user_info: AccountInfo) -> bool:
    deleted, message = Logics.del_account(user_info)
    print(message)
    return not deleted


def _exit(user_info: AccountInfo) -> bool:
    print("Exit the Bank")
    return False


# Keyed by the same choices as MENU_OPTIONS - a handler returns False to end
# the session. Both dicts are checked against each other at import time.
HANDLERS = {
    "1": _balance,
    "2": _deposit,
    "3": _withdraw,
    "4": _add_subscription,
    "5": _remove_subscription,
    "6": _list_subscriptions,
    "7": _balance_next_day,
    "8": _purge,
    "9": _exit,
}

assert HANDLERS.keys() == MENU_OPTIONS.keys(), (
    "every menu option needs a route, and every route needs a menu option"
)


def api():
    user_name = input("input your username: ")
    user_info = Logics.connect_user(user_name)

    if user_info is None:
        print("could not create or find a user, exiting")
        return

    while True:
        choice = input(render_menu()).strip()
        handler = HANDLERS.get(choice)
        if handler is None:
            print("invalid Input")
            continue

        try:
            if not handler(user_info):
                break
        except BankAppError as error:
            print(error)
