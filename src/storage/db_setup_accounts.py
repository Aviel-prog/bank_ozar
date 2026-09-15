import logging
import sqlite3
from src.config import DB_ACCOUNTS_PATH

logger = logging.getLogger(__name__)


def init_accounts_database(db_name: str = DB_ACCOUNTS_PATH):
    """Initializes schema and default records if table does not exist."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                account_type INTEGER NOT NULL DEFAULT 1,
                locked INTEGER NOT NULL DEFAULT 0
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM accounts")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO accounts (username, balance, account_type, locked)
                VALUES (?, ?, ?, ?);
            """, [
                ("t_osherzi", 1500, 1, 0),
                ("t_shimonv", 5000, 2, 0),
                ("t_idome", -100, 3, 1),
                ("t_raz_ba", 10000, 4, 0),
                ("t_noabir", 0, 1, 1)
            ])

        conn.commit()
    logger.info("accounts database ready at '%s'", db_name)