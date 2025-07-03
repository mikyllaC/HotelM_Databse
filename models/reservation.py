from utils.helpers import log, get_connection
from datetime import datetime


def main():
    reservation_model = ReservationModel()




class ReservationModel:
    def __init__(self):
        self.create_reservation_table()

    def create_reservation_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS RESERVATION (
                    RESERVATION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    GUEST_ID INTEGER NOT NULL,
                    ROOM_ID INTEGER NOT NULL,
                    
                    CHECK_IN_DATE DATE NOT NULL,
                    CHECK_OUT_DATE DATE NOT NULL,
                    
                    NUMBER_OF_ADULTS INTEGER DEFAULT 1,
                    NUMBER_OF_CHILDREN INTEGER DEFAULT 0,
                    
                    STATUS VARCHAR(20) DEFAULT 'Booked',
                    
                    NOTES TEXT,
                    EMPLOYEE_ID TEXT,
                    
                    CANCELLATION_DATE TIMESTAMP,
                    CANCELLATION_REASON TEXT,
                    
                    FOREIGN KEY (GUEST_ID) REFERENCES GUEST(GUEST_ID),
                    FOREIGN KEY (ROOM_ID) REFERENCES ROOM(ROOM_ID),
                    FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(EMPLOYEE_ID)
                )""")

            conn.commit()

    def add_reservation(self, reservation_data):
        try:
            # Handle both old ROOM_IDS format and direct ROOM_ID for backward compatibility
            if "ROOM_IDS" in reservation_data and reservation_data["ROOM_IDS"]:
                # Take only the first room from the list
                room_id = reservation_data["ROOM_IDS"][0]
                reservation_data["ROOM_ID"] = room_id
                del reservation_data["ROOM_IDS"]

            # Validate room rate exists before creating reservation
            from models.billing import BillingModel
            billing_model = BillingModel()

            room_id = reservation_data.get("ROOM_ID")
            has_rate, rate_message = billing_model.validate_room_has_rate(room_id)

            if not has_rate:
                log(f"Cannot create reservation: {rate_message}")
                raise ValueError(rate_message)

            # Create the reservation directly
            with get_connection() as conn:
                cursor = conn.cursor()

                query = """
                INSERT INTO RESERVATION (
                    GUEST_ID, ROOM_ID, CHECK_IN_DATE, CHECK_OUT_DATE, 
                    NUMBER_OF_ADULTS, NUMBER_OF_CHILDREN,
                    STATUS, NOTES, EMPLOYEE_ID
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                cursor.execute(query, (
                    reservation_data.get("GUEST_ID"),
                    reservation_data.get("ROOM_ID"),
                    reservation_data.get("CHECK_IN_DATE"),
                    reservation_data.get("CHECK_OUT_DATE"),
                    reservation_data.get("NUMBER_OF_ADULTS", 1),
                    reservation_data.get("NUMBER_OF_CHILDREN", 0),
                    reservation_data.get("STATUS", "Booked"),
                    reservation_data.get("NOTES"),
                    reservation_data.get("EMPLOYEE_ID")
                ))

                # Get the ID of the newly created reservation
                reservation_id = cursor.lastrowid

                conn.commit()
                log(f"Added new reservation with ID: {reservation_id}")

                # Auto-generate invoice for confirmed reservations
                if reservation_data.get("STATUS") in ["Confirmed", "Booked"]:
                    try:
                        from models.billing import BillingModel
                        from models.settings import SettingsModel

                        # Check if auto-generation is enabled in settings
                        settings_model = SettingsModel()
                        auto_generate = settings_model.get_billing_setting('AUTO_GENERATE_INVOICE', True)

                        if auto_generate:
                            billing_model = BillingModel()
                            invoice_id = billing_model.auto_generate_invoice_for_reservation(
                                reservation_id,
                                reservation_data.get("EMPLOYEE_ID")
                            )
                            if invoice_id:
                                log(f"Auto-generated invoice {invoice_id} for reservation {reservation_id}")
                            else:
                                log(f"Failed to auto-generate invoice for reservation {reservation_id}", "WARNING")
                    except Exception as e:
                        log(f"Could not auto-generate invoice for reservation {reservation_id}: {str(e)}", "WARNING")

                return reservation_id

        except Exception as e:
            log(f"Error adding reservation: {str(e)}")
            return None

    def get_reservation_by_id(self, reservation_id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT * FROM RESERVATION WHERE RESERVATION_ID = ?
                """, (reservation_id,))

                reservation = cursor.fetchone()

                if reservation:
                    # Convert to dictionary
                    column_names = [description[0] for description in cursor.description]
                    reservation_dict = dict(zip(column_names, reservation))

                    return reservation_dict
                return None

        except Exception as e:
            log(f"Error getting reservation {reservation_id}: {str(e)}")
            return None

    def get_all_reservations(self, status=None, guest_id=None):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                query = "SELECT * FROM RESERVATION"
                params = []

                # Add filters if provided
                if status or guest_id:
                    query += " WHERE"

                    if status:
                        query += " STATUS = ?"
                        params.append(status)

                    if guest_id:
                        if status:
                            query += " AND"
                        query += " GUEST_ID = ?"
                        params.append(guest_id)

                cursor.execute(query, params)

                reservations = cursor.fetchall()

                # Convert to list of dictionaries
                column_names = [description[0] for description in cursor.description]
                result = []

                for reservation in reservations:
                    reservation_dict = dict(zip(column_names, reservation))
                    result.append(reservation_dict)

                return result

        except Exception as e:
            log(f"Error getting reservations: {str(e)}")
            return []

    def update_reservation(self, reservation_id, updated_data):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Build the update query dynamically based on the provided fields
                allowed_fields = [
                    "CHECK_IN_DATE", "CHECK_OUT_DATE",
                    "NUMBER_OF_ADULTS", "NUMBER_OF_CHILDREN", "STATUS",
                    "NOTES", "EMPLOYEE_ID"
                ]

                update_parts = []
                params = []

                for field in allowed_fields:
                    if field in updated_data:
                        update_parts.append(f"{field} = ?")
                        params.append(updated_data[field])

                if not update_parts:
                    log("No valid fields to update")
                    return False

                query = f"UPDATE RESERVATION SET {', '.join(update_parts)} WHERE RESERVATION_ID = ?"
                params.append(reservation_id)

                cursor.execute(query, params)
                conn.commit()

                # Check if the update was successful
                if cursor.rowcount > 0:
                    log(f"Updated reservation {reservation_id}")
                    return True
                else:
                    log(f"No reservation found with ID {reservation_id}")
                    return False

        except Exception as e:
            log(f"Error updating reservation {reservation_id}: {str(e)}")
            return False

    def cancel_reservation(self, reservation_id, reason=None):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Update reservation status and set cancellation details
                cursor.execute("""
                    UPDATE RESERVATION 
                    SET STATUS = 'Cancelled',
                        CANCELLATION_DATE = ?,
                        CANCELLATION_REASON = ?
                    WHERE RESERVATION_ID = ?
                """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reason, reservation_id))

                conn.commit()

                # Check if the update was successful
                if cursor.rowcount > 0:
                    log(f"Cancelled reservation {reservation_id}")
                    return True
                else:
                    log(f"No reservation found with ID {reservation_id}")
                    return False

        except Exception as e:
            log(f"Error cancelling reservation {reservation_id}: {str(e)}")
            return False

    def delete_reservation(self, reservation_id):
        """Delete a reservation permanently from the database, but only if it's been cancelled"""
        try:
            # First, check if the reservation exists and is cancelled
            reservation = self.get_reservation_by_id(reservation_id)
            if not reservation:
                return False

            # Only allow deletion of cancelled reservations
            if reservation.get("STATUS") != "Cancelled":
                return False

            # Delete the reservation
            with get_connection() as conn:
                cursor = conn.cursor()
                query = "DELETE FROM RESERVATION WHERE RESERVATION_ID = ?"
                cursor.execute(query, (reservation_id,))
                conn.commit()

                # Check if the deletion was successful
                if cursor.rowcount > 0:
                    log(f"Deleted reservation {reservation_id}")
                    return True
                else:
                    log(f"No reservation found with ID {reservation_id} for deletion")
                    return False

        except Exception as e:
            log(f"Error deleting reservation: {str(e)}", "ERROR")
            return False

    def get_reservations_by_guest_and_dates(self, guest_id, check_in_date, check_out_date):
        """Get all reservations for a guest within specific dates (used for grouping related reservations)"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT * FROM RESERVATION 
                    WHERE GUEST_ID = ? AND CHECK_IN_DATE = ? AND CHECK_OUT_DATE = ?
                    ORDER BY RESERVATION_ID
                """, (guest_id, check_in_date, check_out_date))

                reservations = cursor.fetchall()

                # Convert to list of dictionaries
                column_names = [description[0] for description in cursor.description]
                result = []

                for reservation in reservations:
                    reservation_dict = dict(zip(column_names, reservation))
                    result.append(reservation_dict)

                return result

        except Exception as e:
            log(f"Error getting reservations by guest and dates: {str(e)}")
            return []

if __name__ == "__main__":
    main()