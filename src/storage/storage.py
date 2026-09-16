import logging
import sqlite3
from contextlib import contextmanager

from src.config import DB_ACCOUNTS_PATH, DB_SUBSCRIPTION_PATH
from src.models import AccountType
from src.exceptions import DatabaseError, EntityNotFoundError
from src.models import AccountInfo

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, db_account_path: str = DB_ACCOUNTS_PATH, db_path_subscription: str = DB_SUBSCRIPTION_PATH):
        self.db_path_subscription = db_path_subscription
        self.db_account_path = db_account_path

    @staticmethod
    @contextmanager
    def _connect(db_path: str):
        """Yields a connection that is always committed (or rolled back) and closed.

        ``with sqlite3.connect(...)`` only manages the transaction - it never
        closes the connection, which is why connections were leaking. Wrapping
        it here guarantees the close and turns driver failures into DatabaseError.
        """
        conn = sqlite3.connect(db_path)
        try:
            with conn:
                yield conn
        except sqlite3.Error as error:
            raise DatabaseError(f"database operation failed on '{db_path}'") from error
        finally:
            conn.close()

    def is_user_exist(self, username: str) -> bool:
        with self._connect(self.db_account_path) as conn:
            cursor = conn.execute(
                'SELECT username FROM accounts WHERE username = ?', (username,)
            )
            return cursor.fetchone() is not None

    def get_user_information(self, username: str) -> AccountInfo:
        with self._connect(self.db_account_path) as conn:
            cursor = conn.execute(
                'SELECT username, balance, locked, account_type FROM accounts WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()

        if row is None:
            raise EntityNotFoundError(f"no account found for username '{username}'")

        return AccountInfo(
            username=row[0],
            balance=row[1],
            locked=bool(row[2]),
            account_type=AccountType(row[3])
        )

    def add_account(self, account: AccountInfo) -> bool:
        """Opens a new account, returning False if the username is taken.

        A clash is an ordinary outcome of two people picking the same name,
        not a database fault, so it comes back as False rather than an error.
        """
        try:
            with self._connect(self.db_account_path) as conn:
                conn.execute(
                    '''INSERT INTO accounts (username, balance, account_type, locked)
                       VALUES (?, ?, ?, ?)''',
                    (account.username, account.balance,
                     account.account_type.value, int(account.locked))
                )
        except DatabaseError as error:
            if isinstance(error.__cause__, sqlite3.IntegrityError):
                logger.info("account for %s already exists", account.username)
                return False
            raise
        return True

    def update_balance(self, username: str, updated_balance: int) -> None:
        with self._connect(self.db_account_path) as conn:
            conn.execute(
                'UPDATE accounts SET balance = ? WHERE username = ?',
                (updated_balance, username)
            )

    def update_lock(self, username: str, updated_status: bool | int) -> None:
        with self._connect(self.db_account_path) as conn:
            conn.execute(
                'UPDATE accounts SET locked = ? WHERE username = ?',
                (int(updated_status), username)
            )

    def delete_account(self, username: str) -> bool:
        """Deletes a user account from the database by username."""
        with self._connect(self.db_account_path) as conn:
            cursor = conn.execute(
                "DELETE FROM accounts WHERE username = ?",
                (username,)
            )
            return cursor.rowcount > 0

    def add_subscription(self, username: str, subscription_name: str, end_date: str, amount: float) -> bool:
        """Adds a new subscription to the database."""
        try:
            with self._connect(self.db_path_subscription) as conn:
                conn.execute('''
                    INSERT INTO subscriptions (username, name, end_date, amount)
                    VALUES (?, ?, ?, ?)
                ''', (username, subscription_name, end_date, amount))
        except DatabaseError as error:
            if isinstance(error.__cause__, sqlite3.IntegrityError):
                return False
            raise
        return True

    def delete_subscription(self, username: str, subscription_name: str) -> bool:
        """Deletes a specific subscription for a user."""
        with self._connect(self.db_path_subscription) as conn:
            cursor = conn.execute('''
                DELETE FROM subscriptions
                WHERE username = ? AND name = ?
            ''', (username, subscription_name))
            return cursor.rowcount > 0

    def delete_subscriptions(self, username: str) -> int:
        """Removes every subscription belonging to a user, returning how many.

        A username can be registered again after an account closes, so rows
        left behind here would quietly become the next customer's bills.
        """
        with self._connect(self.db_path_subscription) as conn:
            cursor = conn.execute(
                'DELETE FROM subscriptions WHERE username = ?', (username,)
            )
            return cursor.rowcount

    def get_subscriptions(self, username: str) -> list:
        """Returns every subscription belonging to a user.

        Storage hands the rows back rather than printing them - deciding how
        a subscription looks on screen is the menu's job, not the database's.
        """
        with self._connect(self.db_path_subscription) as conn:
            cursor = conn.execute('''
                SELECT name, end_date, amount FROM subscriptions 
                WHERE username = ?
            ''', (username,))
            rows = cursor.fetchall()

        return rows
        


STORAGE_MANAGER = StorageManager()
