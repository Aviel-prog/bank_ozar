import datetime
import sqlite3
from enum import Enum

action_options = ("1. balance\n",
                  "2. add money\n",
                  "3. get money\n",
                  "4. subscription action"
                  "5. delete account\n"
                  "6. exit the app"
                  )


class AccountType(Enum):
    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


class AccountInfo:
    def __init__(self, username, balance, account_type, locked):
        self.username = username
        self.balance = balance
        self.account_type = account_type
        self.locked = locked


# ---------------- DB  -----------------------

def init_database(db_name: str = "db.sqlite3"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # Create users table matching the exact types requested
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                account_type INTEGER NOT NULL DEFAULT 1,
                locked INTEGER NOT NULL DEFAULT 0
            );
        """)

        # Insert initial demo data
        cursor.executemany("""
            INSERT OR IGNORE INTO users (username, balance, account_type, locked)
            VALUES (?, ?, ?, ?);
        """, [
            ("t_osherzi", 1500, 1, False),  # Regular user, active
            ("t_shimonv", 5000, 2, False),  # Premium user, active
            ("t_idome", -100, 3, True),  # Locked user
            ("t_raz_ba", 10000, 4, False),
            ("t_noabir", 0, 1, 1)
        ])

        conn.commit()
        print(f"Database successfully created at '{db_name}'!")


class StorageManager:
    def __init__(self, db_path: str = "db.sqlite3"):
        self.db_path = db_path
        self.connection = None
        self.connect()

    def connect(self):
        """Establishes connection and creates table if it does not exist."""
        start_connect = sqlite3.connect(self.db_path)
        self.connection = start_connect.cursor()
        self.connection.execute('PRAGMA foreign_keys = ON;')

    def close(self):
        """Closes the active database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def is_user_exist(self, username: str) -> bool:
        info = self.connection.execute('SELECT username, balance, locked, account_type'
                                   'FROM account where username = ?', username)
        if info:
            return True
        return False
    def get_user_information(self, username) -> AccountInfo:
        info = self.connection.execute('SELECT username, balance, locked, account_type'
                                       'FROM account where username = ?', username)
        info_user = info.fetchall
        return AccountInfo(username=username, balance=info_user[0][1], locked=info_user[0][2],
                           account_type=info_user[0][3])

    @staticmethod
    def update_balance(username: str, updated_balance: int):
        pass

    @staticmethod
    def update_lock(username: str, updated_status: int):
        pass

    def delete_subscription(self, username: str, subscription_name: str):
        pass

    def delete_account(self, username: str, subscription_name: str):
        pass


# ---------------- Logic -----------------------
class Logics:
    @classmethod
    def connect_user(cls, username: str) -> AccountInfo:
        connection = StorageManager("db.sqlite3")
        if connection.is_user_exist(username):
            return connection.get_user_information(username)
        print("user not exist")
        return cls.register_user(username)

    @classmethod
    def get_balance(cls, user_info: AccountInfo) -> str:
        if user_info.locked:
            return "locked"

        if user_info.account_type == AccountType.GREEN:
            user_info.balance += 2
            StorageManager.update_balance(user_info.username, user_info.balance)
        elif user_info.account_type == AccountType.YELLOW:
            return "X in your bank"
        return "{balance} in your bank".format(balance=user_info.balance)

    def add_money(self, user_info: AccountInfo, amount):
        if user_info.locked:
            return "locked"
        if amount < 0:
            return "cant Zero money"

        if user_info.account_type == AccountType.RED:
            if datetime.date.today().day % 2 != 0 and amount > 300:
                return "no more than 300 on odd day"

        user_info.balance += amount
        StorageManager.update_balance(user_info.username, user_info.balance)
        return "added successfully"

    @classmethod
    def get_money(cls, user_info: AccountInfo, amount: int):
        if user_info.locked:
            return "locked"

        if user_info.account_type == AccountType.BLUE:
            if amount > 100:
                return "you cant get more than 100"
        if user_info.account_type == AccountType.YELLOW:
            if user_info.balance - amount < 0:
                user_info.balance -= amount
                StorageManager.update_balance(user_info.username, user_info.balance)
                StorageManager.update_balance(user_info.username, True)
                return "you have less than 0 in your account now"
        if user_info.account_type != AccountType.YELLOW:
            user_info.balance -= amount
            StorageManager.update_balance(user_info.username, user_info.balance)
            return "got the money successfully"

    def add_subscription(self):
        pass

    def delete_subscription(self, user_info: AccountInfo, subscription_name: str):
        StorageManager.delete_subscription(user_info.username, subscription_name)

    def list_subscription(self):
        pass

    @classmethod
    def register_user(cls, username: str) -> AccountInfo:
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

    def delete_account(cls, user_info: AccountInfo):
        StorageManager.delete_account(user_info.username)
        return "account deleted successfully"


# ---------------- Add user  -----------------------


def get_people_list_from_web():
    pass


# -------------------------------------------------------- # main


def api(client_choice="s"):
    user_name = input("input your username: ")
    user_info = Logics.connect_user(user_name)
    while client_choice.lower() != "exit":
        client_choice = int(input(action_options))
        match client_choice:
            case 1:
                print("balance")
                Logics.get_balance(user_info)
            case 2:
                print("add money")
                amount = input("how much to money add: ")
                Logics.add_money(user_info, amount)
            case 3:
                print("get money")
                amount = input("how much to money get: ")
                Logics.get_money(user_info, amount)
            case 4:
                print("add subscriptions")
            case 5:
                subscription_name = input("Enter subscription name: ")
                Logics.delete_subscription(user_info, subscription_name)
                print("delete subscriptions")

            case 6:
                print("list subscriptions")

            case 7:
                print("delete account")
                Logics.delete_account(user_info)
            case 8:
                print("Exit the Bank")
            case _:
                pass


def main():
    init_database()
    StorageManager()
    api()


if __name__ == "__main__":
    main()
