from src.api import api
from src.log_config import setup_logging
from src.storage.db_setup_subscription import init_subscription_database
from src.storage.db_setup_accounts import init_accounts_database


def main():
    setup_logging()
    init_subscription_database()
    init_accounts_database()
    api()


if __name__ == "__main__":
    main()
