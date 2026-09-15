import sqlite3

from constants import AccountType, DB_SUBSCRIPTION_PATH, DB_ACCOUNTS_PATH
from models import AccountInfo


class StorageManager:
    def __init__(self, db_account_path: str = DB_ACCOUNTS_PATH, db_path_subscription: str = DB_SUBSCRIPTION_PATH):
        self.db_path_subscription = db_path_subscription
        self.db_account_path = db_account_path

    def is_user_exist(self, username: str) -> bool:
        with sqlite3.connect(self.db_account_path) as conn:
            cursor = conn.execute(
                'SELECT username FROM accounts WHERE username = ?', (username,)
            )
            return cursor.fetchone() is not None

    def get_user_information(self, username: str) -> AccountInfo:
        with sqlite3.connect(self.db_account_path) as conn:
            cursor = conn.execute(
                'SELECT username, balance, locked, account_type FROM accounts WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()

        if row is None:
            raise ValueError(f"no account found for username '{username}'")

        return AccountInfo(
            username=row[0],
            balance=row[1],
            locked=bool(row[2]),
            account_type=AccountType(row[3])
        )

    def update_balance(self, username: str, updated_balance: int) -> None:
        with sqlite3.connect(self.db_account_path) as conn:
            conn.execute(
                'UPDATE accounts SET balance = ? WHERE username = ?',
                (updated_balance, username)
            )
            conn.commit()

    def update_lock(self, username: str, updated_status: bool | int) -> None:
        with sqlite3.connect(self.db_account_path) as conn:
            conn.execute(
                'UPDATE accounts SET locked = ? WHERE username = ?',
                (int(updated_status), username)
            )
            conn.commit()

    def delete_account(self, username: str) -> bool:
        """Deletes a user account from the database by username."""
        with sqlite3.connect(self.db_account_path) as conn:
            cursor = conn.execute(
                "DELETE FROM accounts WHERE username = ?",
                (username,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def add_subscription(self, username: str, subscription_name: str, end_date: str, amount: float):
        """Adds a new subscription to the database."""
        try:
            with sqlite3.connect(self.db_path_subscription) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO subscriptions (username, name, end_date, amount)
                    VALUES (?, ?, ?, ?)
                ''', (username, subscription_name, end_date, amount))  # TODO check the inputs
                conn.commit()
                print(f"Subscription '{subscription_name}' added successfully for {username}.")
        except sqlite3.IntegrityError:
            print(f"Error: Subscription '{subscription_name}' already exists for {username}.")

    def delete_subscription(self, username: str, subscription_name: str):
        """Deletes a specific subscription for a user."""
        with sqlite3.connect(self.db_path_subscription) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM subscription
                WHERE username = ? AND name = ?
            ''', (username, subscription_name))
            conn.commit()

            if cursor.rowcount > 0: # TODO understate it
                print(f"Subscription '{subscription_name}' deleted successfully for {username}.")
            else:
                print(f"No subscription found matching '{subscription_name}' for {username}.")

    def show_all_subscriptions(self, username: str):
        """Fetches and displays all subscriptions belonging to a user."""
        with sqlite3.connect(self.db_path_subscription) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, end_date, amount 
                FROM subscription 
                WHERE username = ?
            ''', (username,))
            rows = cursor.fetchall()

            if not rows:
                print(f"No active subscriptions found for user: {username}")
                return []


            print(f"--- Subscriptions for {username} ---")
            for row in rows:
                print(f"Name: {row[0]} | Ends: {row[1]} | Amount: ${row[2]:.2f}")
            return rows


STORAGE_MANAGER = StorageManager()
