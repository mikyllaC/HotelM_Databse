from auth import AuthModel
from utils.helpers import log, get_connection


class EmployeeModel(AuthModel):
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

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYEE (
                    EMPLOYEE_ID, FIRST_NAME, LAST_NAME, POSITION, HIRE_DATE, 
                    CONTACT_NUMBER, EMAIL, DATE_OF_BIRTH, ADDRESS, STATUS) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (employee_id,
                          employee_data.get("FIRST_NAME"),
                          employee_data.get("LAST_NAME"),
                          employee_data.get("POSITION"),
                          employee_data.get("HIRE_DATE"),
                          employee_data.get("CONTACT_NUMBER"),
                          employee_data.get("EMAIL"),
                          employee_data.get("DATE_OF_BIRTH"),
                          employee_data.get("ADDRESS"),
                          employee_data.get("STATUS", "active")
                          ))
            conn.commit()
        log(f"Added employee: ({employee_id}) to the database.")

        self.add_user_credentials(employee_id,
                                  employee_data.get("FIRST_NAME"),
                                  employee_data.get("LAST_NAME"),
                                  employee_data.get("HIRE_DATE"))
        return employee_id