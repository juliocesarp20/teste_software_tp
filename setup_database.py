
import sqlite3
def create_database(path):
    # Create or connect to the SQLite database file
    conn = sqlite3.connect(path)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            balance REAL,
            currency TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            interest_rate REAL,
            term_months INTEGER,
            paid_amount REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            sender_id INTEGER,
            receiver_id INTEGER,
            amount REAL,
            currency TEXT,
            FOREIGN KEY(sender_id) REFERENCES accounts(id),
            FOREIGN KEY(receiver_id) REFERENCES accounts(id)
        )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            birth_date TEXT
        )
''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database('test_database.db')
    print("Database setup completed.")