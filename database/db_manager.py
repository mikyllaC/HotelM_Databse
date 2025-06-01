# ============== Imports ==============
import sqlite3
import os
from asyncio import current_task


def main():
    db = DBManager()
    #db.add_employee("Samuel", "Muralid", "CEO")
    #db.add_employee("Mikylla", "Coronado", "Front Desk")
    #db.add_employee("Sofia", "Caday", "Janitor")
    #db.add_employee("Zydney", "Astudillo", "Manager")


# ============== Database Manager Class ==============
class DBManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "Hotel_Management.db")
        # os.path.abspath(__file__) gives the full path to db_manager.py.
        # os.path.dirname(...) gives the directory (.../database/).
        # os.path.join(...) builds the final path to Hotel_Management.db.
        self.create_tables()


    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-style row access
        return conn


    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # ---- Create EMPLOYEE table ----
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS EMPLOYEE (
                EMPLOYEE_ID TEXT PRIMARY KEY,
                FIRST_NAME TEXT NOT NULL,
                LAST_NAME TEXT NOT NULL,
                POSITION TEXT NOT NULL,
                HIRE_DATE TEXT,
                CONTACT_NUMBER INTEGER UNIQUE,
                EMAIL TEXT UNIQUE,
                DATE_OF_BIRTH TEXT,
                ADDRESS TEXT,
                STATUS TEXT NOT NULL DEFAULT 'active')""")

            # ---- Create USER_AUTH table ----
            conn.execute("""
            CREATE TABLE IF NOT EXISTS USER_AUTH (
                EMPLOYEE_ID TEXT PRIMARY KEY,
                PASSWORD TEXT NOT NULL,
                FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(EMPLOYEE_ID))""")

            conn.commit()


    def generate_employee_id(self, first_name, last_name):
        initials = (first_name[0] + last_name[0]).upper()

        with self.get_connection() as conn:
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
            print(f"Previous ID: {result}")

            if result: # if not the first employee
                previous_id_num = int(result[2:]) # skips the initials
                new_id_num = previous_id_num + 1
            else:
                new_id_num = 1

            new_id = f"{initials}{new_id_num:03d}"  # ex: SM001
            print(f"Generated ID: {new_id}")
            return new_id


    def add_employee(self, first_name, last_name, position, hire_date=None, contact_number=None, email=None,
                     date_of_birth=None, address=None, status="active"):
        employee_id = self.generate_employee_id(first_name, last_name)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYEE (
                    EMPLOYEE_ID, FIRST_NAME, LAST_NAME, POSITION, HIRE_DATE, 
                    CONTACT_NUMBER, EMAIL, DATE_OF_BIRTH, ADDRESS, STATUS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (employee_id, first_name, last_name, position, hire_date, contact_number,
                          email, date_of_birth, address, status))
            conn.commit()
        return employee_id


    def add_user_credentials(self, employee_id, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO USER_AUTH (EMPLOYEE_ID, PASSWORD)
                VALUES (?, ?)
            """, (employee_id, password))
            conn.commit()


    def verify_login(self, employee_id, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT ua.PASSWORD, e.*
            FROM USER_AUTH ua
            JOIN EMPLOYEE e ON ua.EMPLOYEE_ID = e.EMPLOYEE_ID
            WHERE ua.EMPLOYEE_ID = ?
            """, (employee_id, ))
            user = cursor.fetchone()

            if not user:
                return None         # employee not found
            if user['STATUS'] != 'active':
                return None         # deactivated account
            if user['PASSWORD'] != password:
                return  None        # incorrect password

            print(f"Login Successful: {user['EMAIL']}")
            return {
                "employee_id": user["EMPLOYEE_ID"],
                "full_name": f"{user['FIRST_NAME']} {user['LAST_NAME']}",
                "position": user["POSITION"],
                "email": user["EMAIL"]
            }



if __name__ == "__main__":
    main()