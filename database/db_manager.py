# ============== Imports ==============
from utils.helpers import get_connection


def main():
    DBManager()

# ============== Database Manager Class ==============
class DBManager:
    def __init__(self):
        self.create_tables()


    def create_tables(self):
        with get_connection() as conn:
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


if __name__ == "__main__":
    main()