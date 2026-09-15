from src.api import api
from storage.db_setup_subscription import init_subcriptionManager_database
from storage.db_setup_accounts import init_accounts_database


def main():
    init_subcriptionManager_database()
    init_accounts_database()
    api()


if __name__ == "__main__":
    main()
