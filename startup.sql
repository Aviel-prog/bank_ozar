def init_database(db_name: str = DB_PATH):
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

        cursor.executemany("""
            INSERT OR IGNORE INTO accounts (username, balance, account_type, locked)
            VALUES (?, ?, ?, ?);
        """, [
            ("t_osherzi", 1500, 1, False),
            ("t_shimonv", 5000, 2, False),
            ("t_idome", -100, 3, True),
            ("t_raz_ba", 10000, 4, False),
            ("t_noabir", 0, 1, 1)
        ])

        conn.commit()
        print(f"Database successfully created at '{db_name}'!")
