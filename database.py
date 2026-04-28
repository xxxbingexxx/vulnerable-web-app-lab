import sqlite3

def init_db():
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')

    # Insert a test user (plaintext password - intentionally insecure)
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized!")