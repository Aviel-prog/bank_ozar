from enum import Enum

DB_PATH = "db.sqlite3"

ACTION_OPTIONS = (
    "1. balance\n"
    "2. add money\n"
    "3. get money\n"
    "4. add subscription\n"
    "5. delete subscription\n"
    "6. list subscriptions\n"
    "7. delete account\n"
    "8. exit the app\n"
    "> "
)


class AccountType(Enum):
    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


