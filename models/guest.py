#import datetime
#import sqlite3

from utils.helpers import log, get_connection


def main():
    guest_model = GuestModel()
    sample_guest_data = {
        "FIRST_NAME": "Municht",
        "LAST_NAME": "Esquivel",
        "CONTACT_NUMBER": "09321234567",
        "EMAIL": "municht.esquivel@example.com",
        "ADDRESS_LINE1": "17 Amethyst st, Fern Village",
        "ADDRESS_LINE2": "Pasong Tamo",
        "CITY": "Quezon City",
        "STATE": "NCR",
        "POSTAL_CODE": "1107",
        "COUNTRY": "Philippines",
        "STATUS": "Checked Out",
        "EMPLOYEE_ID": "SM0001"
    }
    guest_model.add_guest(sample_guest_data)


class GuestModel:
    def __init__(self):
        self.create_guest_table()


    def create_guest_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GUEST (
                    GUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    EMPLOYEE_ID TEXT,
                    FIRST_NAME TEXT NOT NULL,
                    LAST_NAME TEXT NOT NULL,
                    CONTACT_NUMBER TEXT NOT NULL UNIQUE,
                    EMAIL TEXT NOT NULL UNIQUE,
                    ADDRESS_LINE1 TEXT,
                    ADDRESS_LINE2 TEXT,
                    CITY TEXT,
                    STATE TEXT,
                    POSTAL_CODE TEXT,
                    COUNTRY TEXT,
                    STATUS TEXT NOT NULL DEFAULT 'Checked Out',
                    FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(EMPLOYEE_ID)
                )""")
            conn.commit()


    def add_guest(self, guest_data: dict):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                            INSERT INTO GUEST (
                                FIRST_NAME, LAST_NAME, CONTACT_NUMBER, EMAIL,
                                ADDRESS_LINE1, ADDRESS_LINE2, CITY, STATE,
                                POSTAL_CODE, COUNTRY, STATUS, EMPLOYEE_ID
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                guest_data["FIRST_NAME"],
                guest_data["LAST_NAME"],
                guest_data["CONTACT_NUMBER"],
                guest_data["EMAIL"],
                guest_data.get("ADDRESS_LINE1", ""),
                guest_data.get("ADDRESS_LINE2", ""),
                guest_data.get("CITY", ""),
                guest_data.get("STATE", ""),
                guest_data.get("POSTAL_CODE", ""),
                guest_data.get("COUNTRY", ""),
                guest_data.get("STATUS", "Checked Out"),
                guest_data.get("EMPLOYEE_ID", None)
            ))
            conn.commit()
            log(f"Guest added: {guest_data['FIRST_NAME']} {guest_data['LAST_NAME']}")


    def update_guest(self, guest_id: int, updated_data: dict):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                            UPDATE GUEST SET
                                FIRST_NAME = ?, LAST_NAME = ?, CONTACT_NUMBER = ?, EMAIL = ?,
                                ADDRESS_LINE1 = ?, ADDRESS_LINE2 = ?, CITY = ?, STATE = ?,
                                POSTAL_CODE = ?, COUNTRY = ?, STATUS = ?
                            WHERE GUEST_ID = ?
                        """, (
                updated_data["FIRST_NAME"],
                updated_data["LAST_NAME"],
                updated_data["CONTACT_NUMBER"],
                updated_data["EMAIL"],
                updated_data.get("ADDRESS_LINE1", ""),
                updated_data.get("ADDRESS_LINE2", ""),
                updated_data.get("CITY", ""),
                updated_data.get("STATE", ""),
                updated_data.get("POSTAL_CODE", ""),
                updated_data.get("COUNTRY", ""),
                updated_data.get("STATUS", "Checked Out"),
                guest_id
            ))
            conn.commit()
            log(f"Guest updated: [{guest_id}] - {updated_data['FIRST_NAME']} {updated_data['LAST_NAME']}")


    def get_all_guests(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GUEST")
            guests = cursor.fetchall()
            log(f"Retrieved {len(guests)} guests from the database.")
            return guests


    def get_guest_by_id(self, guest_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM GUEST 
            WHERE GUEST_ID = ?
            """, (guest_id,))

            guest = cursor.fetchone()

            if guest:
                return {
                    "GUEST_ID": guest[0],
                    "EMPLOYEE_ID": guest[1],
                    "FIRST_NAME": guest[2],
                    "LAST_NAME": guest[3],
                    "CONTACT_NUMBER": guest[4],
                    "EMAIL": guest[5],
                    "ADDRESS_LINE1": guest[6],
                    "ADDRESS_LINE2": guest[7],
                    "CITY": guest[8],
                    "STATE": guest[9],
                    "POSTAL_CODE": guest[10],
                    "COUNTRY": guest[11],
                    "STATUS": guest[12]
                }
            log(f"No guest found with ID: {guest_id}")
            return None



if __name__ == "__main__":
    main()