from db_setup import init_database
from src.api import api


def main():
    init_database()
    api()


if __name__ == "__main__":
    main()
