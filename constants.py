import os
from enum import Enum

DB_ACCOUNTS_PATH = os.getenv("DB_ACCOUNTS_PATH", "db.accounts")
DB_SUBSCRIPTION_PATH = os.getenv("DB_SUBSCRIPTION_PATH", "db.subscription")

ACTION_OPTIONS = (
    "\n"
    "┌────────[ BANK OZAR CORE SERVICES ]──────────┐\n"
    "│                                             │\n"
    "│   [1] balance      ── View current funds    │\n"
    "│   [2] deposit      ── Add funds             │\n"
    "│   [3] withdraw     ── Get cash              │\n"
    "│   [4] sub:add      ── New recurring payment │\n"
    "│   [5] sub:remove   ── Cancel subscription   │\n"
    "│   [6] sub:list     ── View subscriptions    │\n"
    "│   [7] balance:next day ──                   │\n"
    "│   [8] purge        ── Close account         │\n"
    "│   [9] exit         ── Terminate session     │\n"
    "│                                             │\n"
    "└─────────────────────────────────────────────┘\n"
    "Command > "
)

class AccountType(Enum):
    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


