import datetime
import sqlite3

from models.auth import AuthModel
from utils.helpers import log, get_connection


def main():
    employee_model = EmployeeModel()
    sample_employee_data = {
        "FIRST_NAME": "Samuel",
        "LAST_NAME": "Muralid",
        "GENDER": "Male",
        "CONTACT_NUMBER": "09171234567",
        "EMAIL": "samuel.muralid@example.com",
        "DATE_OF_BIRTH": "1985-07-15",  # Format: YYYY-MM-DD
        "ADDRESS": "123 Executive Lane, Makati City",
        "POSITION": "CEO",
        "HIRE_DATE": datetime.date.today().isoformat(),  # Today's date
        "SALARY": 250000.00,
        "ASSIGNED_TO": "Floor 1",
        "STATUS": "active"
    }
    employee_model.add_employee(sample_employee_data)


class EmployeeModel():
    def __init__(self):
        self.create_employee_table()


    def create_employee_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EMPLOYEE (
                    EMPLOYEE_ID TEXT PRIMARY KEY,
                    FIRST_NAME TEXT NOT NULL,
                    LAST_NAME TEXT NOT NULL,
                    GENDER TEXT NOT NULL,
                    CONTACT_NUMBER TEXT NOT NULL UNIQUE,
                    EMAIL TEXT NOT NULL UNIQUE,
                    DATE_OF_BIRTH DATE NOT NULL,
                    ADDRESS TEXT,
                    POSITION TEXT NOT NULL,
                    HIRE_DATE DATE,
                    SALARY REAL,
                    ASSIGNED_TO TEXT,
                    STATUS TEXT NOT NULL DEFAULT 'Available'
                )""")
            conn.commit()


    def generate_employee_id(self, first_name, last_name):
        initials = (first_name[0] + last_name[0]).upper()

        with get_connection() as conn:
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
                previous_id_num = int(result[0][2:]) # skips the initials
                new_id_num = previous_id_num + 1
            else:
                new_id_num = 1

            new_id = f"{initials}{new_id_num:04d}"  # ex: SM0001
            log(f"Generated new EMPLOYEE_ID: {new_id}")
            return new_id


    def add_employee(self, employee_data: dict):
        employee_id = self.generate_employee_id(employee_data["FIRST_NAME"], employee_data["LAST_NAME"])
        employee_data["EMPLOYEE_ID"] = employee_id

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYEE (
                    EMPLOYEE_ID, FIRST_NAME, LAST_NAME, GENDER, CONTACT_NUMBER,
                    EMAIL, DATE_OF_BIRTH, ADDRESS, POSITION, HIRE_DATE,
                    SALARY, ASSIGNED_TO, STATUS
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (employee_id,
                      employee_data.get("FIRST_NAME"),
                      employee_data.get("LAST_NAME"),
                      employee_data.get("GENDER"),
                      employee_data.get("CONTACT_NUMBER"),
                      employee_data.get("EMAIL"),
                      employee_data.get("DATE_OF_BIRTH"),
                      employee_data.get("ADDRESS"),
                      employee_data.get("POSITION"),
                      employee_data.get("HIRE_DATE"),
                      employee_data.get("SALARY"),
                      employee_data.get("ASSIGNED_TO"),
                      employee_data.get("STATUS", "Available")
                      ))
            conn.commit()

        log(f"Added employee: ({employee_id}) to the database.")

        auth_model = AuthModel()
        auth_model.add_user_credentials(employee_id,
                                  employee_data.get("FIRST_NAME"),
                                  employee_data.get("LAST_NAME"),
                                  employee_data.get("HIRE_DATE"))
        return employee_id


    def get_all_employees(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT *
            FROM EMPLOYEE""")
            return cursor.fetchall()


    def get_employee_details(self, employee_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM EMPLOYEE WHERE EMPLOYEE_ID = ?", (employee_id,))
            row = cursor.fetchone()
            if row:
                # Convert to dict for easier access
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None


    def update_employee_details(self, employee_id, updated_data: dict):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                set_clause = ", ".join(f"{key} = ?" for key in updated_data)
                values = list(updated_data.values()) + [employee_id]
                cursor.execute(f"""
                    UPDATE EMPLOYEE
                    SET {set_clause}
                    WHERE EMPLOYEE_ID = ?
                """, values)
                conn.commit()

        except sqlite3.Error as e:
            log(f"[DB-ERROR] Failed to update employee details: {e}")
            return


    def assign_staff(self, employee_id, assigned_to):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE EMPLOYEE
                SET ASSIGNED_TO = ?
                WHERE EMPLOYEE_ID = ?
                """, (assigned_to, employee_id))
                conn.commit()

                rows_updated = cursor.rowcount
                return rows_updated == 1 # Return True if exactly one row was updated

        except sqlite3.Error as e:
            log(f"[DB-ERROR] Failed to assign staff: {e}")
            return False



if __name__ == "__main__":
    main()