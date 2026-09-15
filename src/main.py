from src.api import api
from src.storage.db_setup_subscription import init_subscription_database
from src.storage.db_setup_accounts import init_accounts_database


def main():
    init_subscription_database()
    init_accounts_database()
    api()


if __name__ == "__main__":
    main()
