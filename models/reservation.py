from utils.helpers import log, get_connection
from datetime import datetime


def main():
    reservation_model = ReservationModel()


class ReservationModel:
    def __init__(self):
        self.create_reservation_table()


    def create_reservation_table(self):
        """Create the RESERVATION table if it doesn't exist"""
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
        """Add a new reservation to the database"""
        try:
            # Validate room rate exists before creating reservation
            from models.billing import BillingModel
            from models.room import RoomModel
            from models.guest import GuestModel

            billing_model = BillingModel()
            room_model = RoomModel()
            guest_model = GuestModel()

            room_id = reservation_data.get("ROOM_ID")
            guest_id = reservation_data.get("GUEST_ID")

            has_rate, rate_message = billing_model.validate_room_has_rate(room_id)
            # If no rate exists, log the message and raise an error
            if not has_rate:
                log(f"Cannot create reservation: {rate_message}")
                raise ValueError(rate_message)

            # Create the reservation
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
                    guest_id,
                    room_id,
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

                # Update guest status to "Reserved"
                guest_data = guest_model.get_guest_by_id(guest_id)
                if guest_data:
                    guest_data["STATUS"] = "Reserved"
                    guest_model.update_guest(guest_id, guest_data)
                    log(f"Updated guest {guest_id} status to 'Reserved'")

                # Update room status to "Reserved"
                room_data = room_model.get_room_by_id(room_id)
                if room_data:
                    room_data["STATUS"] = "Reserved"
                    room_model.update_room(room_data)
                    log(f"Updated room {room_id} status to 'Reserved'")

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
        """Get a reservation by its ID"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT * FROM RESERVATION WHERE RESERVATION_ID = ?
                """, (reservation_id,))

                reservation = cursor.fetchone()

                # If reservation is found, convert it to a dictionary
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
        """Get all reservations"""
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

                # Iterate through the fetched reservations and convert each to a dictionary
                for reservation in reservations:
                    reservation_dict = dict(zip(column_names, reservation))
                    result.append(reservation_dict)

                return result

        except Exception as e:
            log(f"Error getting reservations: {str(e)}")
            return []


    def update_reservation(self, reservation_id, updated_data):
        """Update an existing reservation with new data"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Build the update query dynamically based on the provided fields from updated_data
                allowed_fields = [
                    "CHECK_IN_DATE", "CHECK_OUT_DATE",
                    "NUMBER_OF_ADULTS", "NUMBER_OF_CHILDREN", "STATUS",
                    "NOTES", "EMPLOYEE_ID"
                ]
                # Ensure only allowed fields are updated
                update_parts = []
                params = []

                for field in allowed_fields:
                    if field in updated_data:
                        update_parts.append(f"{field} = ?")
                        params.append(updated_data[field])

                # If no fields to update, return False
                if not update_parts:
                    log("No valid fields to update")
                    return False

                # If no reservation ID provided, return False
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
        """Cancel a reservation and update its status"""
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

                    # Update invoice status to Cancelled
                    try:
                        # Update invoices directly using SQL to avoid any object conversion issues
                        with get_connection() as conn2:
                            cursor2 = conn2.cursor()
                            cursor2.execute("""
                                UPDATE INVOICE 
                                SET STATUS = 'Cancelled', UPDATED_DATE = CURRENT_TIMESTAMP
                                WHERE RESERVATION_ID = ?
                            """, (reservation_id,))
                            conn2.commit()

                            # Log the number of rows updated
                            updated_count = cursor2.rowcount
                            log(f"Invoice update attempted for reservation {reservation_id}, rows affected: {updated_count}")
                            # If no invoices were updated, log a warning
                            if updated_count > 0:
                                log(f"Updated {updated_count} invoice(s) status to Cancelled for reservation {reservation_id}")
                            else:
                                log(f"No invoices found for reservation {reservation_id}", "WARNING")

                            # Fetch and log the current status of invoices for this reservation
                            cursor2.execute("SELECT INVOICE_ID, STATUS FROM INVOICE WHERE RESERVATION_ID = ?", (reservation_id,))
                            invoices = cursor2.fetchall()
                            if invoices:
                                for inv in invoices:
                                    log(f"Invoice {inv[0]} status after cancel: {inv[1]}")
                            else:
                                log(f"No invoice records found for reservation {reservation_id} after update.", "WARNING")

                    except Exception as e:
                        log(f"Error updating invoice status for cancelled reservation {reservation_id}: {str(e)}", "WARNING")

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
            status = reservation.get("STATUS") if isinstance(reservation, dict) else reservation["STATUS"]
            if status != "Cancelled":
                return False

            # Delete associated invoices first to maintain referential integrity
            from models.billing import BillingModel
            billing_model = BillingModel()

            # Get all invoices for this reservation
            invoices = billing_model.get_invoices_by_reservation(reservation_id)

            # Delete payments for each invoice
            if invoices:
                with get_connection() as conn:
                    cursor = conn.cursor()

                    for invoice in invoices:
                        # Get invoice ID from the first column if it's a tuple, or from INVOICE_ID if it's a dict
                        invoice_id = invoice[0] if isinstance(invoice, tuple) else invoice["INVOICE_ID"]

                        # Delete all payments for this invoice
                        cursor.execute("DELETE FROM PAYMENT WHERE INVOICE_ID = ?", (invoice_id,))
                        log(f"Deleted payments for invoice {invoice_id}")

                        # Delete the invoice itself
                        cursor.execute("DELETE FROM INVOICE WHERE INVOICE_ID = ?", (invoice_id,))
                        log(f"Deleted invoice {invoice_id} for reservation {reservation_id}")

                    conn.commit()

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



if __name__ == "__main__":
    main()