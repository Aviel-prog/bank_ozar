"""Shared helpers for the logic tests.

The rules and Logics both reach for the module level STORAGE_MANAGER, so a
test has to replace that name in every module that imported it. StorageTestCase
does exactly that, which is why each test runs against memory and never opens
db.accounts.
"""

import logging
import unittest
from unittest import mock

from src.exceptions import EntityNotFoundError
from src.models import AccountInfo, AccountType

# The app logs to a file once main() runs; under test nothing configures
# logging, so warnings would fall through to stderr and litter the output.
logging.getLogger("src").addHandler(logging.NullHandler())
logging.getLogger("src").propagate = False

#: Every module that did ``from src.storage.storage import STORAGE_MANAGER``.
STORAGE_MODULES = (
    "src.logics.logics",
    "src.logics.base_rules",
    "src.logics.red_rules",
    "src.logics.green_rules",
    "src.logics.yellow_rules",
)


class FakeStorage:
    """In-memory stand-in for StorageManager, recording what it was asked to do."""

    def __init__(self, accounts=None, subscriptions=None):
        # Copied, not shared: a class level fixture would otherwise carry
        # mutations from one test method into the next.
        self.accounts: dict[str, AccountInfo] = {
            name: AccountInfo(stored.username, stored.balance,
                              stored.account_type, stored.locked)
            for name, stored in (accounts or {}).items()
        }
        #: rows of (username, name, end_date, amount)
        self.subscriptions: list[tuple] = list(subscriptions or [])
        self.calls: list[tuple] = []

    # --- accounts -------------------------------------------------------
    def get_user_information(self, username: str) -> AccountInfo:
        self.calls.append(("get_user_information", username))
        if username not in self.accounts:
            raise EntityNotFoundError(f"no account found for username '{username}'")
        stored = self.accounts[username]
        # A fresh object, as the real manager builds one from a row.
        return AccountInfo(stored.username, stored.balance,
                           stored.account_type, stored.locked)

    def add_account(self, account: AccountInfo) -> bool:
        self.calls.append(("add_account", account.username))
        if account.username in self.accounts:
            return False
        self.accounts[account.username] = AccountInfo(
            account.username, account.balance, account.account_type, account.locked
        )
        return True

    def update_balance(self, username: str, updated_balance: int) -> None:
        self.calls.append(("update_balance", username, updated_balance))
        if username in self.accounts:
            self.accounts[username].balance = updated_balance

    def update_lock(self, username: str, updated_status) -> None:
        self.calls.append(("update_lock", username, bool(updated_status)))
        if username in self.accounts:
            self.accounts[username].locked = bool(updated_status)

    def delete_account(self, username: str) -> bool:
        self.calls.append(("delete_account", username))
        return self.accounts.pop(username, None) is not None

    def is_user_exist(self, username: str) -> bool:
        return username in self.accounts

    # --- subscriptions --------------------------------------------------
    def add_subscription(self, username, name, end_date, amount) -> bool:
        self.calls.append(("add_subscription", username, name, end_date, amount))
        if any(row[0] == username and row[1] == name for row in self.subscriptions):
            return False
        self.subscriptions.append((username, name, end_date, amount))
        return True

    def delete_subscription(self, username, name) -> bool:
        before = len(self.subscriptions)
        self.subscriptions = [row for row in self.subscriptions
                              if not (row[0] == username and row[1] == name)]
        return len(self.subscriptions) < before

    def delete_subscriptions(self, username) -> int:
        self.calls.append(("delete_subscriptions", username))
        before = len(self.subscriptions)
        self.subscriptions = [row for row in self.subscriptions if row[0] != username]
        return before - len(self.subscriptions)

    def get_subscriptions(self, username) -> list:
        return [(name, end, amount)
                for user, name, end, amount in self.subscriptions if user == username]

    # --- assertions helpers ---------------------------------------------
    def called(self, method: str) -> list[tuple]:
        """Every recorded call to a method, so a test can assert on arguments."""
        return [call for call in self.calls if call[0] == method]


class StorageTestCase(unittest.TestCase):
    """Base case that swaps the storage singleton out for a FakeStorage."""

    accounts: dict = {}
    subscriptions: list = []

    def setUp(self):
        self.storage = FakeStorage(self.accounts, self.subscriptions)
        for module in STORAGE_MODULES:
            patcher = mock.patch(f"{module}.STORAGE_MANAGER", self.storage)
            patcher.start()
            self.addCleanup(patcher.stop)

    def given_account(self, *args, **kwargs) -> AccountInfo:
        """Stores an account and returns the live object to operate on.

        Storage keeps its own copy on purpose. If it held the very object the
        test passes into the rules, a write through storage would update that
        object too, and the test could no longer tell whether the code under
        test changed it or the fake did.
        """
        live = account(*args, **kwargs)
        self.storage.accounts[live.username] = AccountInfo(
            live.username, live.balance, live.account_type, live.locked
        )
        return live


def account(username="t_test", balance=100,
            account_type=AccountType.RED, locked=False) -> AccountInfo:
    """An AccountInfo with everything defaulted, so a test names only what it cares about."""
    return AccountInfo(username, balance, account_type, locked)


def person(username="p_test", **overrides) -> dict:
    """A directory record that qualifies for nothing, before overrides."""
    record = {
        "username": username,
        "serviceType": "חובה",
        "phone": "050-1111",
        "lastName": "כהן",
        "department": "אחר",
        "rank": "טוראי",
        "firstName": "דן",
        "nickname": "",
        "gender": "F",
        "organization": "אחר",
    }
    record.update(overrides)
    return record


BLUE_PERSON = person("p_blue", serviceType="קבע", phone="03-5551234")
RED_PERSON = person("p_red", lastName="לוין", department="פסיפס")
GREEN_PERSON = person("p_green", rank="סמל", firstName="יוסי")
YELLOW_PERSON = person("p_yellow", nickname="ג'ינג'י")
