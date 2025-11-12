import sqlite3

def get_db_connection():
    conn = sqlite3.connect("fraud_detection.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            amount REAL,
            location TEXT,
            device TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()
