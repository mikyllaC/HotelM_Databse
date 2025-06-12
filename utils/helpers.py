import os
import sqlite3
from datetime import datetime


def clear_screen(widget):  # destroys all child widgets under the given widget/frame
    for widget in widget.winfo_children():
        widget.destroy()


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_db_path():
    # Returns the absolute path to the Hotel_Management.db file.
    # Assumes the DB file is in the `database/` directory at project root.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "database", "Hotel_Management.db")


def get_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # makes every row you fetch (with fetchone() or fetchall()) behave like a dictionary
    return conn
