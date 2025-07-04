import random
from tkinter import messagebox

from utils.helpers import log, get_connection, clear_screen


class AuthModel:
    def __init__(self):
        self.create_auth_table()


    def create_auth_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()

            conn.execute("""
                   CREATE TABLE IF NOT EXISTS USER_AUTH (
                       EMPLOYEE_ID TEXT PRIMARY KEY,
                       PASSWORD TEXT NOT NULL,
                       FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(EMPLOYEE_ID))""")

            conn.commit()


    def add_user_credentials(self, employee_id, first_name, last_name, hire_date, password=None):
        if not password:
            default_password = self.generate_default_password(first_name, last_name, hire_date)
            # log(f"[DEV] Generated default password for {employee_id}: {default_password}")
        else:
            default_password = password

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                 INSERT INTO USER_AUTH (EMPLOYEE_ID, PASSWORD)
                 VALUES (?, ?)
             """, (employee_id, default_password))
            conn.commit()
        log(f"Stored authentication credentials for {employee_id}")


    def generate_default_password(self, first_name, last_name, hire_date):
        # default password format:
        # <FirstInitial><LastInitial><@><HireYear><#><Random2Digits> | SM@2024#83
        initials = (first_name[0] + last_name[0]).upper()
        hire_year = hire_date.split("-")[0]  # extract year from hire_date
        random_digits = random.randint(10, 99)
        default_password = f"{initials}@{hire_year}#{random_digits}"
        return default_password


    def get_user_credentials(self, employee_id):
        with get_connection() as conn:
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


    def update_user_credentials(self, employee_id, new_password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
             UPDATE USER_AUTH
             SET PASSWORD = ?
             WHERE EMPLOYEE_ID = ?""", (new_password, employee_id,))
            conn.commit()
        log("Updated user's authentication credentials.")


    def login(self, employee_id, password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT UA.PASSWORD, E.*
                FROM USER_AUTH UA
                JOIN EMPLOYEE E ON UA.EMPLOYEE_ID = E.EMPLOYEE_ID
                WHERE UA.EMPLOYEE_ID = ?""", (employee_id,))
            result = cursor.fetchone()

            if result and result["PASSWORD"] == password:
                return dict(result)
            else:
                return None


    def logout(self, parent):
        from ui.auth.loginScreen import LoginScreen
        from utils.session import Session

        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if not confirm:
            return  # if user cancels logout, do nothing

        if Session.current_user:
            log(f"Logging out: [{Session.current_user.get('EMPLOYEE_ID', 'Unknown')}]")
        else:
            log("Logging out: No user currently in session.")
        Session.current_user = None

        # clear dashboard and return to login screen
        clear_screen(parent)
        login_screen = LoginScreen(parent, parent.on_login_success)
        login_screen.pack(fill="both", expand=True)


    def signup(self, employee_data: dict, password: str):
        try:
            from models.employee import EmployeeModel

            # Validate required fields
            required_fields = ["FIRST_NAME", "LAST_NAME", "GENDER", "CONTACT_NUMBER",
                             "EMAIL", "DATE_OF_BIRTH", "ADDRESS", "POSITION"]
            for field in required_fields:
                if not employee_data.get(field):
                    return False, f"Missing required field: {field}", None

            # validation - Check if email or contact already exists
            if self.check_existing_credentials(employee_data.get("EMAIL"), employee_data.get("CONTACT_NUMBER")):
                return False, "Email or contact number already exists", None

            # Create employee record
            employee_model = EmployeeModel()
            employee_id = employee_model.add_employee(employee_data)

            # Update authentication with custom password
            if password:
                self.update_user_credentials(employee_id, password)

            log(f"Successfully registered new employee: {employee_id}")
            return True, f"Registration successful! Employee ID: {employee_id}", employee_id

        except Exception as e:
            log(f"Signup error: {str(e)}")
            return False, f"Registration failed: {str(e)}", None


    def check_existing_credentials(self, email: str, contact_number: str):
        """Check if email or contact number already exists in the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM EMPLOYEE 
                WHERE EMAIL = ? OR CONTACT_NUMBER = ?
            """, (email, contact_number))
            count = cursor.fetchone()[0]
            return count > 0
