import datetime
import sqlite3

from utils.helpers import log, get_connection


def main():
    guest_model = GuestModel()
    sample_guest_data = {
        "FIRST_NAME": "Municht",
        "LAST_NAME": "Esquivel",
        "CONTACT_NUMBER": "09321234567",
        "EMAIL": "municht.esquivel@example.com",
        "ADDRESS": "123 Executive Lane, Makati City",
        "STATUS": "Checked Out"
    }
    guest_model.add_guest(sample_guest_data)


class GuestModel():
    def __init__(self):
        self.create_guest_table()


    def create_guest_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GUEST (
                    GUEST_ID INTEGER PRIMARY KEY,
                    FIRST_NAME TEXT NOT NULL,
                    LAST_NAME TEXT NOT NULL,
                    CONTACT_NUMBER TEXT NOT NULL UNIQUE,
                    EMAIL TEXT NOT NULL UNIQUE,
                    ADDRESS TEXT,
                    STATUS TEXT NOT NULL DEFAULT 'Checked Out'
                )""")
            conn.commit()


    def add_guest(self, guest_data: dict):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO GUEST (FIRST_NAME, LAST_NAME, CONTACT_NUMBER, EMAIL, ADDRESS, STATUS)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (guest_data["FIRST_NAME"],
                 guest_data["LAST_NAME"],
                 guest_data["CONTACT_NUMBER"],
                 guest_data["EMAIL"],
                 guest_data.get("ADDRESS", ""),
                 guest_data.get("STATUS", "Checked Out")))
            conn.commit()
            log(f"Guest added: {guest_data['FIRST_NAME']} {guest_data['LAST_NAME']}")


    def get_all_guests(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GUEST")
            guests = cursor.fetchall()
            log(f"Retrieved {len(guests)} guests from the database.")
            return guests



if __name__ == "__main__":
    main()