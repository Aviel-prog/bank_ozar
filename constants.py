from enum import Enum

DB_PATH = "db.sqlite3"

ACTION_OPTIONS = (
    "\n"
    "┌────────[ BANK OZAR CORE SERVICES ]──────────┐\n"
    "│                                             │\n"
    "│   [1] balance      ── View current funds    │\n"
    "│   [2] deposit      ── Add funds             │\n"
    "│   [3] withdraw     ── Get cash              │\n"
    "│   [4] sub:list     ── View subscriptions    │\n"
    "│   [5] sub:add      ── New recurring payment │\n"
    "│   [6] sub:remove   ── Cancel subscription   │\n"
    "│   [7] purge        ── Close account         │\n"
    "│   [8] exit         ── Terminate session     │\n"
    "│                                             │\n"
    "└─────────────────────────────────────────────┘\n"
    "Command > "
)


class AccountType(Enum):
    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


