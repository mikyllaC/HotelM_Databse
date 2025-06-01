# ============== Imports ==============
import sqlite3
import os

def main():
    db = DBManager()


# ============== Database Manager Class ==============
class DBManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "Hotel_Management.db")
        # os.path.abspath(__file__) gives the full path to db_manager.py.
        # os.path.dirname(...) gives the directory (.../database/).
        # os.path.join(...) builds the final path to Hotel_Management.db.

        self.create_employee_table()


    def create_employee_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS EMPLOYEE
                employee_id TEXT PRIMARY KEY
                first_name TEXT NOT NULL
                last_name TEXT NOT NULL
                position TEXT NOT NULL""")
            conn.commit()



if __name__ == "__main__":
    main()