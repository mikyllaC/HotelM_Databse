# ============== Imports ==============
import sqlite3
import os

def main():
    db = DBManager()

# ============== Database Manager Class ==============
class DBManager:
    def __init__(self):
        # Dynamically set the database path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "Hotel_Management.db")


if __name__ == "__main__":
    main()