import sqlite3


def get_connection():
    return sqlite3.connect("hms_database.db")


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Example table creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)

    conn.commit()
    conn.close()