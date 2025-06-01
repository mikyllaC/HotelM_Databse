# ============== Imports ==============
import sqlite3
import os
from asyncio import current_task


def main():
    db = DBManager()
    db.add_employee("Samuel", "Muralid", "CEO")


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
            CREATE TABLE IF NOT EXISTS EMPLOYEE (
                EMPLOYEE_ID TEXT PRIMARY KEY,
                FIRST_NAME TEXT NOT NULL,
                LAST_NAME TEXT NOT NULL,
                POSITION TEXT NOT NULL)""")
            conn.commit()


    def generate_employee_id(self, first_name, last_name):
        initials = (first_name[0] + last_name[0]).upper()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # finds the highest value id (previous id)
            cursor.execute("""
            SELECT EMPLOYEE_ID 
            FROM EMPLOYEE
            ORDER BY CAST(SUBSTR(EMPLOYEE_ID, 3) AS INTEGER) DESC
            LIMIT 1
            """)
            # SUBSTR(employee_id, 3) — skips the first two characters (the initials).
            # CAST(... AS INTEGER) — converts the numeric suffix to an integer.
            # Orders descending by this integer to find the max. LIMIT gets the max
            result = cursor.fetchone()[0]

            if result: # if not the first employee
                previous_id_num = int(result[2:]) # skips the initials
                new_id_num = previous_id_num + 1
            else:
                new_id_num = 1

            new_id = f"{initials}+{new_id_num:04d}"  # ex: SM0001

            return new_id


    def add_employee(self, first_name, last_name, position):
        self.generate_employee_id(first_name, last_name)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()




if __name__ == "__main__":
    main()