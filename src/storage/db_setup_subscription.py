import sqlite3
from src.config import DB_SUBSCRIPTION_PATH


def init_subscription_database(db_name: str = DB_SUBSCRIPTION_PATH):
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
                ("t_osherzi", "Premium Plan", "31-12-2026", 15.00),
                ("t_idome", "Cloud Storage", "01-10-2026", 10.00),
                ("t_raz_ba", "Enterprise Package", "01-06-2027", 100.00),
                ("t_noabir", "Streaming Pass", "30-09-2026", 0.00)
            ])
            conn.commit()

        print(f"subscriptions Database successfully created/connected at '{db_name}'!")
