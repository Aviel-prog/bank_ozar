import sqlite3

from constants import DB_PATH, AccountType
from models import AccountInfo


def init_database(db_name: str = DB_PATH):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                account_type INTEGER NOT NULL DEFAULT 1,
                locked INTEGER NOT NULL DEFAULT 0
            );
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO users (username, balance, account_type, locked)
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
        self.conn = None
        self.connection = None
        self.connect()

    def connect(self):
        """Establishes connection and creates table if it does not exist."""
        self.conn = sqlite3.connect(self.db_path)
        self.connection = self.conn.cursor()
        self.connection.execute('PRAGMA foreign_keys = ON;')

    def close(self):
        """Closes the active database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.connection = None

    def is_user_exist(self, username: str) -> bool:
        self.connection.execute(
            'SELECT username FROM users WHERE username = ?', (username,)
        )
        return self.connection.fetchone() is not None

    def get_user_information(self, username) -> AccountInfo:
        self.connection.execute(
            'SELECT username, balance, locked, account_type FROM users WHERE username = ?',
            (username,)
        )
        row = self.connection.fetchone()
        print(f"dibug + {row}")
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
                'UPDATE users SET balance = ? WHERE username = ?',
                (updated_balance, username)
            )
            conn.commit()

    @staticmethod
    def update_lock(username: str, updated_status: int, db_path: str = DB_PATH):
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                'UPDATE users SET locked = ? WHERE username = ?',
                (int(updated_status), username)
            )
            conn.commit()

    def delete_subscription(self, username: str, subscription_name: str):
        pass

    def delete_account(self, username: str):
        pass
