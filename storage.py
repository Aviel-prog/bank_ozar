import sqlite3

from constants import DB_PATH, AccountType
from models import AccountInfo


def init_database(db_name: str = DB_PATH):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                account_type INTEGER NOT NULL DEFAULT 1,
                locked INTEGER NOT NULL DEFAULT 0
            );
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO accounts (username, balance, account_type, locked)
            VALUES (?, ?, ?, ?);
        """, [
            ("t_osherzi", 1500, 1, False),
            ("t_shimonv", 5000, 2, False),
            ("t_idome", -100, 3, True),
            ("t_raz_ba", 10000, 4, False),
            ("t_noabir", 0, 1, 1)
        ])

        conn.commit()
        print(f"Database successfully created at '{db_name}'!")


class StorageManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def is_user_exist(self, username: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT username FROM accounts WHERE username = ?', (username,)
            )
            return cursor.fetchone() is not None

    def get_user_information(self, username) -> AccountInfo:
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
            locked=row[2],
            account_type=AccountType(row[3])
        )

    @staticmethod
    def update_balance(username: str, updated_balance: int, db_path: str = DB_PATH):
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                'UPDATE accounts SET balance = ? WHERE username = ?',
                (updated_balance, username)
            )
            conn.commit()

    @staticmethod
    def update_lock(username: str, updated_status: int, db_path: str = DB_PATH):
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                'UPDATE accounts SET locked = ? WHERE username = ?',
                (int(updated_status), username)
            )
            conn.commit()

    def delete_subscription(self, username: str, subscription_name: str):
        pass

    @staticmethod
    def delete_account(username: str, db_path: str = DB_PATH):
        """Deletes a user account from the database by username."""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM accounts WHERE username = ?",
                (username,)
            )
            conn.commit()
            return cursor.rowcount > 0


STORAGE_MANAGER = StorageManager()