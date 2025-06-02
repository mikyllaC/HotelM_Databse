# ============== Imports ==============
import sqlite3
import os
import random
from utils.helpers import log


def main():
    db = DBManager()
    employee_data = {
        "FIRST_NAME": "Samuel",
        "LAST_NAME": "Muralid",
        "POSITION": "CEO",
        "HIRE_DATE": "2024-06-01",
        "CONTACT_NUMBER": "1234567890",
        "EMAIL": "samuel@hotel.com",
        "DATE_OF_BIRTH": "2005-06-27",
        "ADDRESS": "123 Amethyst St, Fern Village, QC"
    }
    db.add_employee(employee_data)
    #db.add_user_credentials("SM0001")


# ============== Database Manager Class ==============
class DBManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "Hotel_Management.db")
        log(f"Database path set to: {self.db_path}")

        self.create_tables()


    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # makes every row you fetch (with fetchone() or fetchall()) behave like a dictionary
        return conn


    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # ---- Create EMPLOYEE table ----
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='EMPLOYEE'")
            if cursor.fetchone(): # Check if EMPLOYEE table exists
                log("EMPLOYEE table already exists.")
            else:
                cursor.execute("""
                    CREATE TABLE EMPLOYEE (
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
                log("EMPLOYEE table created.")

            # ---- Create USER_AUTH table ----
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER_AUTH'")
            if cursor.fetchone(): # Check if USER_AUTH table exists
                log("USER_AUTH table already exists.")
            else:
                cursor.execute("""
                    CREATE TABLE USER_AUTH (
                        EMPLOYEE_ID TEXT PRIMARY KEY,
                        PASSWORD TEXT NOT NULL,
                        FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(EMPLOYEE_ID))""")
                log("USER_AUTH table created.")

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
            result = cursor.fetchone()

            if result: # if not the first employee
                previous_id_num = int(result[2:]) # skips the initials
                new_id_num = previous_id_num + 1
            else:
                new_id_num = 1

            new_id = f"{initials}{new_id_num:04d}"  # ex: SM0001
            log(f"Generated new EMPLOYEE_ID: {new_id}")
            return new_id


    def add_employee(self, employee_data: dict):
        employee_id = self.generate_employee_id(employee_data["FIRST_NAME"], employee_data["LAST_NAME"])
        employee_data["employee_id"] = employee_id

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYEE (
                    EMPLOYEE_ID, FIRST_NAME, LAST_NAME, POSITION, HIRE_DATE, 
                    CONTACT_NUMBER, EMAIL, DATE_OF_BIRTH, ADDRESS, STATUS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (employee_id,
                          employee_data.get("FIRST_NAME"),employee_data.get("LAST_NAME"),employee_data.get("POSITION"),
                          employee_data.get("HIRE_DATE"),employee_data.get("CONTACT_NUMBER"),
                          employee_data.get("EMAIL"),employee_data.get("DATE_OF_BIRTH"),
                          employee_data.get("ADDRESS"),employee_data.get("STATUS", "active") ) )
            conn.commit()
        log(f"Added employee: ({employee_id}) to the database.")

        self.add_user_credentials(employee_id, employee_data.get("FIRST_NAME"), employee_data.get("LAST_NAME"),
                                  employee_data.get("HIRE_DATE"))
        return employee_id


    def generate_default_password(self, first_name, last_name, hire_date):
        # default password format:
        # <FirstInitial><LastInitial><@><HireYear><#><Random2Digits> | SM@2024#83
        initials = (first_name[0] + last_name[0]).upper()
        hire_year = hire_date.split("-")[0]  # extract year from hire_date
        random_digits = random.randint(10, 99)
        default_password = f"{initials}@{hire_year}#{random_digits}"
        return default_password


    def add_user_credentials(self, employee_id, first_name, last_name, hire_date, password=None):
        if not password:
            default_password = self.generate_default_password(first_name, last_name, hire_date)
            log(f"Generated default password for {employee_id}: {default_password}")
        else:
            default_password = password

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO USER_AUTH (EMPLOYEE_ID, PASSWORD)
                VALUES (?, ?)
            """, (employee_id, default_password))
            conn.commit()
        log(f"Stored authentication credentials for {employee_id}")


    def get_user_credentials(self, employee_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT UA.PASSWORD, E.*
            FROM USER_AUTH UA
            JOIN EMPLOYEE E ON UA.EMPLOYEE_ID = E.EMPLOYEE_ID
            WHERE UA.EMPLOYEE_ID = ?
            """, (employee_id,))
            # ua is a shorthand for the USER_AUTH table.
            # e is a shorthand for the EMPLOYEE table.
            # ua.PASSWORD → selects the PASSWORD column from the USER_AUTH table.
            # e.* → selects all the columns from the EMPLOYEE table.
            # joins the columns into 1 row for each employee, WHERE filters the EMPLOYEE_ID to only get 1 result
            return cursor.fetchone()


if __name__ == "__main__":
    main()