"""Runtime configuration, read from the environment with local defaults."""

import os

DB_ACCOUNTS_PATH = os.getenv("DB_ACCOUNTS_PATH", "db.accounts")
DB_SUBSCRIPTION_PATH = os.getenv("DB_SUBSCRIPTION_PATH", "db.subscription")

SUBSCRIPTION_DATE_FORMAT = "%d-%m-%Y"

LOG_PATH = os.getenv("LOG_PATH", "bank.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
