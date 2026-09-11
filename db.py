def add_user(cursor, conn):
    # Define the data parameters for the new record
    new_user = {
        'username': 'jcharles',
        'lastname': 'Charles',
        'nickname': 'Jim',
        'organization': 'Global Logistics',
        'service_type': 'Enterprise',
        'phone': '+1-555-0344',
        'gender': 'Male',
        'balance': 450.00,
        'locked': 0  # 0 means the account is active/unlocked
    }

    # Execute the insertion
    try:
        cursor.execute("""
        INSERT INTO users (username, lastname, nickname, organization, service_type, phone, gender, balance, locked)
        VALUES (:username, :lastname, :nickname, :organization, :service_type, :phone, :gender, :balance, :locked);
        """, new_user)

        # Commit the transaction to save changes
        conn.commit()
        print(f"Successfully added record for user: {new_user['username']}")

    except sqlite3.IntegrityError as e:
        print(f"Error: Could not add user. The username might already exist. ({e})")


def create_database():
    # Connect to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect("app_database.db")
    cursor = conn.cursor()

    # Create the table with your specified schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        lastname TEXT NOT NULL,
        nickname TEXT,
        organization TEXT,
        service_type TEXT,
        phone TEXT,
        gender TEXT CHECK(gender IN ('Male', 'Female')),
        balance REAL DEFAULT 0.0 CHECK(balance >= 0),
        locked INTEGER DEFAULT 0 CHECK(locked IN (0, 1))
    );
    """)

    # Save changes and close the connection
    conn.commit()
    add_user(cursor, conn)
    conn.close()
    print("Database and table created successfully!")


if __name__ == "__main__":
    create_database()

import sqlite3
