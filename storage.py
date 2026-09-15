import sqlite3

from constants import DB_PATH, AccountType
from models import AccountInfo


class StorageManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def is_user_exist(self, username: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT username FROM accounts WHERE username = ?', (username,)
            )
            return cursor.fetchone() is not None

    def get_user_information(self, username: str) -> AccountInfo:
        with sqlite3.connect(self.db_path) as conn:
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
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'UPDATE accounts SET balance = ? WHERE username = ?',
                (updated_balance, username)
            )
            conn.commit()

    def update_lock(self, username: str, updated_status: bool | int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'UPDATE accounts SET locked = ? WHERE username = ?',
                (int(updated_status), username)
            )
            conn.commit()

    def delete_subscription(self, username: str, subscription_name: str):
        pass

    def delete_account(self, username: str) -> bool:
        """Deletes a user account from the database by username."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM accounts WHERE username = ?",
                (username,)
            )
            conn.commit()
            return cursor.rowcount > 0


STORAGE_MANAGER = StorageManager()