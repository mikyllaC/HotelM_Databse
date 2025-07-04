from utils.helpers import log, get_connection


def main():
    guest_model = GuestModel()


class GuestModel:
    def __init__(self):
        self.create_guest_table()


    def create_guest_table(self):
        """Create the GUEST table if it doesn't exist"""
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
        """Add a new guest to the database"""
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
        """Update an existing guest's information"""
        try:
            # Get current guest data to check for status changes
            old_status = None
            current_guest = self.get_guest_by_id(guest_id)
            if current_guest:
                old_status = current_guest.get("STATUS")

            # Update the guest information
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

            # Handle status changes that impact rooms
            new_status = updated_data.get("STATUS")
            if old_status != new_status:
                log(f"Guest status changed from '{old_status}' to '{new_status}'")

                # If guest is now checked in, update room status to occupied
                if new_status == "Checked In":
                    self.update_room_status(guest_id, "Occupied")
                    log(f"Guest {guest_id} checked in - updated associated room to Occupied")

                # If guest is now reserved, update room status to reserved
                elif new_status == "Reserved":
                    self.update_room_status(guest_id, "Reserved")
                    log(f"Guest {guest_id} reserved - updated associated room to Reserved")

                # If guest is now checked out, update room status to available
                elif new_status == "Checked Out":
                    self.update_room_status(guest_id, "Available")
                    log(f"Guest {guest_id} checked out - updated associated room to Available")

            return True

        except Exception as e:
            log(f"Error updating guest {guest_id}: {str(e)}", "ERROR")
            return False

    def update_room_status(self, guest_id: int, new_room_status: str):
        """Update the status of rooms associated with a guest and their reservations"""
        try:
            # Find active reservations for this guest
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT RESERVATION_ID, ROOM_ID FROM RESERVATION
                    WHERE GUEST_ID = ? AND STATUS IN ('Booked', 'Confirmed', 'Reserved')
                    AND DATE(CHECK_OUT_DATE) >= DATE('now')
                """, (guest_id,))

                reservations = cursor.fetchall()

                if not reservations:
                    log(f"No active reservations found for guest {guest_id}")
                    return

                # Update status for all associated rooms and reservations
                from models.room import RoomModel
                room_model = RoomModel()

                for reservation in reservations:
                    reservation_id, room_id = reservation

                    # Update room status
                    room_data = room_model.get_room_by_id(room_id)
                    if room_data:
                        room_data["STATUS"] = new_room_status
                        room_model.update_room(room_data)
                        log(f"Updated room {room_id} status to '{new_room_status}'")

                    # Also update reservation status based on the new room status
                    if new_room_status == "Occupied":
                        # Update reservation to "Checked In" when room is occupied
                        cursor.execute("""
                            UPDATE RESERVATION
                            SET STATUS = 'Checked In'
                            WHERE RESERVATION_ID = ?
                        """, (reservation_id,))
                        log(f"Updated reservation {reservation_id} status to 'Checked In'")
                    elif new_room_status == "Reserved":
                        # Update reservation to "Reserved"
                        cursor.execute("""
                            UPDATE RESERVATION
                            SET STATUS = 'Reserved'
                            WHERE RESERVATION_ID = ?
                        """, (reservation_id,))
                        log(f"Updated reservation {reservation_id} status to 'Reserved'")
                    elif new_room_status == "Available":
                        # Update reservation to "Checked Out" when room becomes available
                        cursor.execute("""
                            UPDATE RESERVATION
                            SET STATUS = 'Checked Out'
                            WHERE RESERVATION_ID = ?
                        """, (reservation_id,))
                        log(f"Updated reservation {reservation_id} status to 'Checked Out'")

                # Commit the changes
                conn.commit()

        except Exception as e:
            log(f"Error updating room and reservation status for guest {guest_id}: {str(e)}", "ERROR")


    def get_all_guests(self):
        """Retrieve all guests from the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GUEST")
            guests = cursor.fetchall()
            log(f"Retrieved {len(guests)} guests from the database.")
            return guests


    def get_guest_by_id(self, guest_id: int):
        """Retrieve a guest by their ID"""
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


    def check_guest_has_reservations(self, guest_id: int):
        """Check if a guest has any existing active (non-cancelled) reservations"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check only for active reservations (status != 'Cancelled')
                cursor.execute("""
                SELECT COUNT(*) FROM RESERVATION
                WHERE GUEST_ID = ? AND STATUS != 'Cancelled'
                """, (guest_id,))

                active_count = cursor.fetchone()[0]

                # Also get total reservation count for informational purposes
                cursor.execute("""
                SELECT COUNT(*) FROM RESERVATION
                WHERE GUEST_ID = ?
                """, (guest_id,))

                total_count = cursor.fetchone()[0]

                return active_count > 0, active_count, total_count
        except Exception as e:
            log(f"Error checking guest reservations: {str(e)}", "ERROR")
            return True, 0, 0  # Assume has reservations on error for safety


    def delete_guest(self, guest_id: int):
        """Delete a guest if they have no existing active reservations"""
        try:
            # First check if the guest exists
            guest = self.get_guest_by_id(guest_id)
            if not guest:
                log(f"Cannot delete: No guest found with ID: {guest_id}")
                return False, "Guest not found"

            # Check if the guest has any active reservations
            has_active_reservations, active_count, total_count = self.check_guest_has_reservations(guest_id)

            if has_active_reservations:
                log(f"Cannot delete guest {guest_id}: Has {active_count} active reservations")
                return False, f"Cannot delete guest with existing active reservations ({active_count} found)"

            # Begin transaction
            with get_connection() as conn:
                cursor = conn.cursor()

                try:
                    # First, delete any cancelled reservations for this guest
                    cursor.execute("DELETE FROM RESERVATION WHERE GUEST_ID = ? AND STATUS = 'Cancelled'", (guest_id,))
                    cancelled_count = cursor.rowcount

                    # Then, delete the guest
                    cursor.execute("DELETE FROM GUEST WHERE GUEST_ID = ?", (guest_id,))
                    guest_deleted = cursor.rowcount

                    # Commit the transaction
                    conn.commit()

                    # Check if the guest was successfully deleted
                    if guest_deleted > 0:
                        log_message = f"Successfully deleted guest with ID: {guest_id}"
                        if cancelled_count > 0:
                            log_message += f" and {cancelled_count} cancelled reservation(s)"
                        log(log_message)

                        success_message = "Guest deleted successfully"
                        if cancelled_count > 0:
                            success_message += f" ({cancelled_count} cancelled reservation(s) were also removed)"
                        return True, success_message
                    else:
                        log(f"Failed to delete guest with ID: {guest_id}")
                        return False, "Failed to delete guest"

                except Exception as e:
                    # Roll back the transaction on error
                    conn.rollback()
                    raise

        except Exception as e:
            log(f"Error deleting guest: {str(e)}", "ERROR")
            return False, f"Error: {str(e)}"
