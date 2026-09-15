import sqlite3
from constants import DB_SUBSCRIPTION_PATH


def init_subcriptionManager_database(db_name: str = DB_SUBSCRIPTION_PATH):
    """Creates the subscription table if it does not exist."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # 1. Create the correct table structure
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    username TEXT,
                    name TEXT,
                    end_date TEXT,
                    amount REAL,
                    PRIMARY KEY (username, name)
                )
            ''')
        conn.commit()

        # 2. Check the correct table name ('subscriptions')
        cursor.execute("SELECT COUNT(*) FROM subscriptions")
        if cursor.fetchone()[0] == 0:
            # 3. Provide sample data that matches your subscription columns
            # Layout order: (username, name, end_date, amount)
            cursor.executemany("""
                INSERT INTO subscriptions (username, name, end_date, amount)
                VALUES (?, ?, ?, ?);
            """, [
                ("t_osherzi", "Premium Plan", "2026-12-31", 15.00),
                ("t_shimonv", "Basic Access", "2027-01-15", 50.00),
                ("t_idome", "Cloud Storage", "2026-10-01", 10.00),
                ("t_raz_ba", "Enterprise Package", "2027-06-01", 100.00),
                ("t_noabir", "Streaming Pass", "2026-09-30", 0.00)
            ])
            conn.commit()

        print(f"subscriptions Database successfully created/connected at '{db_name}'!")
