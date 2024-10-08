import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL NOT NULL
    )
    ''')

    # Create Transactions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Insert users
    users = [
        ('armen_davtian', generate_password_hash('password123'), 1000.0),
        ('petr_pavel', generate_password_hash('asdf12345'), 1500.0)
    ]

    cursor.executemany('INSERT OR IGNORE INTO users (username, password, balance) VALUES (?, ?, ?)', users)
    conn.commit()
    conn.close()
    print("Database initialized with sample users.")

if __name__ == '__main__':
    init_db()
