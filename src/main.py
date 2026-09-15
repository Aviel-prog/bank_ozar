from logics.logics import Logics
from src.api import api
from storage.storage import StorageManager
from storage.db_setup_subscription import init_subcriptionManager_database
from storage.db_setup_accounts import init_accounts_database


def main():
    """Prepares the databases and wires the application together.

    This is the only place that knows how the pieces are assembled: it builds
    the storage, hands it to the bank logic and hands that to the menu, so no
    layer has to reach past the one directly below it.
    """
    init_subcriptionManager_database()
    init_accounts_database()

    storage = StorageManager()
    api(Logics(storage))


if __name__ == "__main__":
    main()
