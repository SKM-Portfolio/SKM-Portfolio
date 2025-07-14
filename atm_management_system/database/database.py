# Database connection and setup
import sqlite3

def connect_db():
    """Connects to the database."""
    conn = sqlite3.connect('atm.db')
    return conn

def create_tables():
    """Creates the database tables."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            account_number TEXT NOT NULL UNIQUE,
            pin TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Database tables created successfully.")
