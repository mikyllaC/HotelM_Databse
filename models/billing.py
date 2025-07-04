from utils.helpers import log, get_connection
from datetime import datetime


def main():
    billing_model = BillingModel()


class BillingModel:
    def __init__(self):
        self.create_billing_tables()

        # Initialize settings model for getting configuration values
        from models.settings import SettingsModel
        self.settings_model = SettingsModel()


    def create_billing_tables(self):
        """Create billing-related tables if they do not exist"""
        with get_connection() as conn:
            cursor = conn.cursor()

            # Create INVOICE table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS INVOICE (
                    INVOICE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    RESERVATION_ID INTEGER NOT NULL,
                    ISSUE_DATE DATE NOT NULL,
                    DUE_DATE DATE,
                    
                    SUBTOTAL DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    TAX_RATE DECIMAL(5,4) NOT NULL DEFAULT 0.12,
                    TAX_AMOUNT DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    TOTAL_AMOUNT DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    
                    STATUS VARCHAR(20) DEFAULT 'Pending',
                    NOTES TEXT,
                    
                    CREATED_BY TEXT,
                    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UPDATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (RESERVATION_ID) REFERENCES RESERVATION(RESERVATION_ID),
                    FOREIGN KEY (CREATED_BY) REFERENCES EMPLOYEE(EMPLOYEE_ID)
                )""")

            # Create PAYMENT table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PAYMENT (
                    PAYMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    INVOICE_ID INTEGER NOT NULL,
                    
                    PAYMENT_DATE DATE NOT NULL,
                    AMOUNT_PAID DECIMAL(10,2) NOT NULL,
                    PAYMENT_METHOD VARCHAR(50) NOT NULL,
                    
                    TRANSACTION_ID TEXT,
                    REFERENCE_NUMBER TEXT,
                    
                    STATUS VARCHAR(20) DEFAULT 'Completed',
                    NOTES TEXT,
                    
                    PROCESSED_BY TEXT,
                    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (INVOICE_ID) REFERENCES INVOICE(INVOICE_ID),
                    FOREIGN KEY (PROCESSED_BY) REFERENCES EMPLOYEE(EMPLOYEE_ID)
                )""")

            # Create ROOM_RATE table for dynamic pricing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ROOM_RATE (
                    RATE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ROOM_TYPE_ID INTEGER NOT NULL,
                    
                    RATE_NAME VARCHAR(100) NOT NULL,
                    BASE_RATE DECIMAL(10,2) NOT NULL,
                    EXTRA_ADULT_RATE DECIMAL(10,2) DEFAULT 0.00,
                    EXTRA_CHILD_RATE DECIMAL(10,2) DEFAULT 0.00,
                    
                    EFFECTIVE_DATE DATE NOT NULL,
                    EXPIRY_DATE DATE,
                    
                    IS_ACTIVE BOOLEAN DEFAULT 1,
                    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (ROOM_TYPE_ID) REFERENCES ROOM_TYPE(ROOM_TYPE_ID)
                )""")

            conn.commit()
            log("Billing tables created successfully.")


    def auto_generate_invoice_for_reservation(self, reservation_id, created_by=None):
        """Automatically generate invoice when reservation is created/confirmed"""
        try:
            # Check if invoice already exists
            existing_invoice = self.get_invoices_by_reservation(reservation_id)
            if existing_invoice:
                log(f"Invoice already exists for reservation {reservation_id}")
                return existing_invoice[0]['INVOICE_ID'] if isinstance(existing_invoice[0], dict) else existing_invoice[0][0]

            # Generate new invoice
            invoice_id = self.generate_invoice(reservation_id, created_by)
            if invoice_id:
                log(f"Auto-generated invoice {invoice_id} for reservation {reservation_id}")
            return invoice_id

        except Exception as e:
            log(f"Error auto-generating invoice: {str(e)}", "ERROR")
            return None


    def get_tax_rate(self):
        """Get tax rate from settings"""
        return self.settings_model.get_billing_setting('TAX_RATE', 0.12)

    def get_service_charge_rate(self):
        """Get service charge rate from settings"""
        return self.settings_model.get_billing_setting('SERVICE_CHARGE', 0.10)

    def get_currency_symbol(self):
        """Get currency symbol from settings"""
        return self.settings_model.get_billing_setting('CURRENCY_SYMBOL', '₱')

    def get_decimal_places(self):
        """Get decimal places for currency from settings"""
        return self.settings_model.get_billing_setting('DECIMAL_PLACES', 2)


    def generate_invoice(self, reservation_id, created_by=None):
        """Generate a comprehensive invoice for a reservation using all billing settings"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check if invoice already exists for this reservation
                cursor.execute("SELECT INVOICE_ID FROM INVOICE WHERE RESERVATION_ID = ?", (reservation_id,))
                existing_invoice = cursor.fetchone()

                # If invoice already exists, return it
                if existing_invoice:
                    log(f"Invoice already exists for reservation {reservation_id}")
                    return existing_invoice[0]

                # Get reservation details
                from models.reservation import ReservationModel
                from models.room import RoomModel

                reservation_model = ReservationModel()
                room_model = RoomModel()

                reservation = reservation_model.get_reservation_by_id(reservation_id)
                if not reservation:
                    log(f"Reservation {reservation_id} not found")
                    return None

                # Calculate total charges with comprehensive billing
                subtotal = self.calculate_total_charges(reservation, room_model)

                if subtotal is None:
                    log(f"Could not calculate charges for reservation {reservation_id}")
                    return None

                # Get tax rate and calculate tax
                tax_rate = self.get_tax_rate()
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount

                # Calculate due date based on settings
                due_date = self.calculate_due_date()

                # Create invoice with detailed information
                cursor.execute("""
                    INSERT INTO INVOICE (
                        RESERVATION_ID, ISSUE_DATE, DUE_DATE,
                        SUBTOTAL, TAX_RATE, TAX_AMOUNT, TOTAL_AMOUNT,
                        STATUS, CREATED_BY, NOTES
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    reservation_id, datetime.now().date(), due_date,
                    subtotal, tax_rate, tax_amount, total_amount,
                    'Pending', created_by, self.generate_invoice_notes(reservation)
                ))

                invoice_id = cursor.lastrowid
                conn.commit()

                log(f"Comprehensive invoice {invoice_id} generated for reservation {reservation_id}")
                log(f"Invoice details: Subtotal=${subtotal:.2f}, Tax=${tax_amount:.2f}, Total=${total_amount:.2f}")

                return invoice_id

        except Exception as e:
            log(f"Error generating invoice: {str(e)}", "ERROR")
            return None

    def calculate_due_date(self):
        """Calculate invoice due date based on billing settings - s"""
        try:
            # Get due days from settings
            due_days = self.settings_model.get_billing_setting('INVOICE_DUE_DAYS', 0)
            due_date = datetime.now().date()

            # If due days are specified, add them to the current date
            if due_days > 0:
                from datetime import timedelta
                due_date = due_date + timedelta(days=due_days)

            return due_date
        except Exception as e:
            log(f"Error calculating due date: {str(e)}", "ERROR")
            return datetime.now().date()

    def generate_invoice_notes(self, reservation):
        """Generate invoice notes based on reservation details - s"""
        try:
            notes = []

            # Add reservation-specific notes
            if reservation.get("NOTES"):
                notes.append(f"Guest requests: {reservation.get('NOTES')}")

            # Add billing policy notes
            grace_period = self.settings_model.get_billing_setting('PAYMENT_GRACE_PERIOD', 3)
            if grace_period > 0:
                notes.append(f"Payment grace period: {grace_period} days")

            late_fee = self.settings_model.get_billing_setting('LATE_PAYMENT_FEE', 25.0)
            if late_fee > 0:
                notes.append(f"Late payment fee: ${late_fee:.2f}")

            return " | ".join(notes) if notes else None

        except Exception as e:
            log(f"Error generating invoice notes: {str(e)}", "ERROR")
            return None

    def calculate_total_charges(self, reservation, room_model):
        """Calculate total charges for a reservation including room rate, extra guests, and time-based fees"""
        try:
            # Get room details
            room_id = reservation.get("ROOM_ID")
            room_data = room_model.get_room_data_with_type(room_id)

            if not room_data:
                return None

            # Calculate nights
            check_in_date = datetime.strptime(reservation.get("CHECK_IN_DATE"), "%Y-%m-%d")
            check_out_date = datetime.strptime(reservation.get("CHECK_OUT_DATE"), "%Y-%m-%d")
            nights = (check_out_date - check_in_date).days

            if nights <= 0:
                nights = 1

            # Get room rate and guest details
            room_type_id = room_data.get('ROOM_TYPE_ID')
            base_rate = self.get_room_rate(room_type_id)

            # Check if room rate exists
            if base_rate is None:
                log(f"No rate found for room type ID {room_type_id}. Cannot calculate charges.", "ERROR")
                return None

            # Get guest counts
            num_adults = reservation.get("NUMBER_OF_ADULTS", 1)
            num_children = reservation.get("NUMBER_OF_CHILDREN", 0)

            # Calculate base accommodation charges
            total_charges = nights * base_rate

            # Add extra guest charges using room type rates
            extra_charges = self.calculate_extra_guest_charges(room_type_id, num_adults, num_children, nights)
            total_charges += extra_charges

            # Add time-based fees (early check-in, late checkout)
            time_based_fees = self.calculate_time_based_fees(reservation)
            total_charges += time_based_fees

            # Apply service charge
            service_charge_rate = self.get_service_charge_rate()
            if service_charge_rate > 0:
                service_charge = total_charges * service_charge_rate
                total_charges += service_charge

            return total_charges

        except Exception as e:
            log(f"Error calculating charges: {str(e)}", "ERROR")
            return None


    def validate_room_has_rate(self, room_id):
        """Validate if a room has a configured rate, so that reservations can be made"""
        try:
            from models.room import RoomModel
            room_model = RoomModel()

            # Get room data
            room_data = room_model.get_room_data_with_type(room_id)
            if not room_data:
                return False, "Room not found"

            room_type_id = room_data.get('ROOM_TYPE_ID')
            room_type_name = room_data.get('TYPE_NAME', 'Unknown')

            # Check if rate exists
            base_rate = self.get_room_rate(room_type_id)

            # If no rate is found, return an error message
            if base_rate is None:
                return False, f"No rate configured for room type '{room_type_name}'. Please set up room rates before making reservations."

            return True, "Rate found"

        except Exception as e:
            log(f"Error validating room rate: {str(e)}", "ERROR")
            return False, f"Error validating room rate: {str(e)}"


    def get_room_rate(self, room_type_id):
        """Get the current room rate for a room type"""
        try:
            # Get rate from ROOM_RATE table
            current_rate = self.get_current_room_rate(room_type_id)
            if current_rate:
                columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                          "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                          "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                rate_dict = dict(zip(columns, current_rate))
                # Return the base rate as a float
                return float(rate_dict['BASE_RATE'])

            # If no rate found, return None to indicate missing rate
            log(f"No rate found for room type ID {room_type_id}", "WARNING")
            return None

        except Exception as e:
            log(f"Error getting room rate for room type {room_type_id}: {str(e)}", "ERROR")
            return None

    def calculate_extra_guest_charges(self, room_type_id, num_adults, num_children, nights):
        """Calculate charges for extra guests based on room type capacity"""
        try:
            from models.room import RoomModel
            room_model = RoomModel()

            # Get room type details
            room_type = room_model.get_room_type_by_id(room_type_id)
            if not room_type:
                return 0

            # Get base adult and child numbers from room type
            base_adults = room_type.get('BASE_ADULT_NUM', 2)
            base_children = room_type.get('BASE_CHILD_NUM', 0)

            # Calculate extra guests
            extra_adults = max(0, num_adults - base_adults)
            extra_children = max(0, num_children - base_children)

            # Get rates from room type
            extra_adult_rate = room_type.get('EXTRA_ADULT_RATE', 0)
            extra_child_rate = room_type.get('EXTRA_CHILD_RATE', 0)

            # Get current room rate which should have the correct extra guest rates
            current_rate = self.get_current_room_rate(room_type_id)
            if current_rate:
                columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                          "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                          "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                rate_dict = dict(zip(columns, current_rate))
                # Use the rates from the room rate record if available
                if rate_dict['EXTRA_ADULT_RATE'] > 0:
                    extra_adult_rate = float(rate_dict['EXTRA_ADULT_RATE'])
                if rate_dict['EXTRA_CHILD_RATE'] > 0:
                    extra_child_rate = float(rate_dict['EXTRA_CHILD_RATE'])

            # If room type doesn't have rates, use settings defaults as fallback
            if extra_adult_rate == 0:
                extra_adult_rate = float(self.settings_model.get_billing_setting('DEFAULT_EXTRA_ADULT_RATE', 0.0))
            if extra_child_rate == 0:
                extra_child_rate = float(self.settings_model.get_billing_setting('DEFAULT_EXTRA_CHILD_RATE', 0.0))

            # Ensure rates are properly converted to float
            extra_adult_rate = float(extra_adult_rate)
            extra_child_rate = float(extra_child_rate)

            # Calculate total extra charges
            total_extra_charges = (extra_adults * extra_adult_rate * nights) + (extra_children * extra_child_rate * nights)

            return total_extra_charges

        except Exception as e:
            log(f"Error calculating extra guest charges: {str(e)}", "ERROR")
            return 0

    def calculate_time_based_fees(self, reservation):
        """Calculate early check-in and late checkout fees based on actual times - s"""
        try:
            total_fees = 0

            # Early check-in fee (if requested in reservation notes or special field)
            notes = reservation.get("NOTES", "").lower()
            if "early check" in notes or "early arrival" in notes:
                early_checkin_fee = self.settings_model.get_billing_setting('EARLY_CHECKIN_FEE', 25.0)
                total_fees += early_checkin_fee

            # Late checkout fee
            if "late check" in notes or "late departure" in notes:
                late_checkout_fee = self.settings_model.get_billing_setting('LATE_CHECKOUT_FEE', 50.0)
                total_fees += late_checkout_fee

            return total_fees

        except Exception as e:
            log(f"Error calculating time-based fees: {str(e)}", "ERROR")
            return 0


    def get_invoices_by_reservation(self, reservation_id):
        """Get all invoices for a reservation"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM INVOICE 
                    WHERE RESERVATION_ID = ?
                    ORDER BY CREATED_DATE DESC
                """, (reservation_id,))

                return cursor.fetchall()

        except Exception as e:
            log(f"Error getting invoices for reservation: {str(e)}", "ERROR")
            return []


    def get_billing_summary_by_reservation(self, reservation_id):
        """Get a summary of billing information for a reservation"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Get the latest invoice for this reservation
                cursor.execute("""
                    SELECT INVOICE_ID, SUBTOTAL, TAX_AMOUNT, TOTAL_AMOUNT, STATUS
                    FROM INVOICE 
                    WHERE RESERVATION_ID = ?
                    ORDER BY CREATED_DATE DESC
                    LIMIT 1
                """, (reservation_id,))

                invoice = cursor.fetchone()

                # If no invoice exists, auto-generate one
                if not invoice:
                    log(f"No invoice found for reservation {reservation_id}, auto-generating...")
                    invoice_id = self.auto_generate_invoice_for_reservation(reservation_id)
                    if invoice_id:
                        # Fetch the newly created invoice
                        cursor.execute("""
                            SELECT INVOICE_ID, SUBTOTAL, TAX_AMOUNT, TOTAL_AMOUNT, STATUS
                            FROM INVOICE 
                            WHERE INVOICE_ID = ?
                        """, (invoice_id,))
                        invoice = cursor.fetchone()

                # If we still don't have an invoice, return None
                if invoice:
                    invoice_id, subtotal, tax_amount, total_amount, status = invoice

                    # Get total payments for this invoice
                    cursor.execute("""
                        SELECT COALESCE(SUM(AMOUNT_PAID), 0)
                        FROM PAYMENT 
                        WHERE INVOICE_ID = ?
                    """, (invoice_id,))

                    total_paid = cursor.fetchone()[0]

                    # Determine payment status
                    if status == "Cancelled":
                        payment_status = "Cancelled"
                    elif total_paid >= total_amount:
                        payment_status = "Paid"
                    elif total_paid > 0:
                        payment_status = "Partial"
                    else:
                        payment_status = "Pending"

                    # Return summary as a dictionary
                    return {
                        'invoice_id': f"INV{invoice_id:04d}",
                        'total_amount': total_amount,
                        'amount_paid': total_paid,
                        'payment_status': payment_status,
                        'status': status
                    }

                return None

        except Exception as e:
            log(f"Error getting billing summary: {str(e)}", "ERROR")
            return None


    def get_invoice_by_reservation(self, reservation_id):
        """Get detailed invoice for a reservation"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Get invoice with reservation details
                cursor.execute("""
                    SELECT i.*, r.CHECK_IN_DATE, r.CHECK_OUT_DATE, r.GUEST_ID, r.ROOM_ID
                    FROM INVOICE i
                    JOIN RESERVATION r ON i.RESERVATION_ID = r.RESERVATION_ID
                    WHERE i.RESERVATION_ID = ?
                    ORDER BY i.CREATED_DATE DESC
                    LIMIT 1
                """, (reservation_id,))

                invoice_row = cursor.fetchone()

                # If no invoice exists, auto-generate one
                if not invoice_row:
                    log(f"No invoice found for reservation {reservation_id}, auto-generating...")
                    invoice_id = self.auto_generate_invoice_for_reservation(reservation_id)
                    if invoice_id:
                        # Fetch the newly created invoice
                        cursor.execute("""
                            SELECT i.*, r.CHECK_IN_DATE, r.CHECK_OUT_DATE, r.GUEST_ID, r.ROOM_ID
                            FROM INVOICE i
                            JOIN RESERVATION r ON i.RESERVATION_ID = r.RESERVATION_ID
                            WHERE i.INVOICE_ID = ?
                        """, (invoice_id,))
                        invoice_row = cursor.fetchone()

                if not invoice_row:
                    return None

                # Convert row to dictionary
                columns = [description[0] for description in cursor.description]
                invoice = dict(zip(columns, invoice_row))

                # Get payments for this invoice
                cursor.execute("""
                    SELECT PAYMENT_ID, PAYMENT_DATE, AMOUNT_PAID, PAYMENT_METHOD, 
                           TRANSACTION_ID, REFERENCE_NUMBER, STATUS, NOTES
                    FROM PAYMENT 
                    WHERE INVOICE_ID = ?
                    ORDER BY PAYMENT_DATE DESC
                """, (invoice['INVOICE_ID'],))

                payments = []
                # Fetch all payments and convert to dictionary
                for payment_row in cursor.fetchall():
                    payment_columns = [description[0] for description in cursor.description]
                    payment = dict(zip(payment_columns, payment_row))
                    payments.append(payment)
                # Add payments to invoice
                invoice['PAYMENTS'] = payments

                # Calculate subtotal if not already set - s
                nights = 1
                try:
                    check_in_date = datetime.strptime(invoice['CHECK_IN_DATE'], "%Y-%m-%d")
                    check_out_date = datetime.strptime(invoice['CHECK_OUT_DATE'], "%Y-%m-%d")
                    nights = (check_out_date - check_in_date).days
                except:
                    pass

                room_rate = invoice['SUBTOTAL'] / nights if nights > 0 else invoice['SUBTOTAL']

                invoice['ITEMS'] = [{
                    'DESCRIPTION': f"Room Accommodation ({nights} nights)",
                    'QUANTITY': nights,
                    'UNIT_PRICE': room_rate,
                    'TOTAL_PRICE': invoice['SUBTOTAL']
                }]

                return invoice

        except Exception as e:
            log(f"Error getting detailed invoice: {str(e)}", "ERROR")
            return None


    def process_payment(self, invoice_id, payment_data):
        """Process a payment for an invoice"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check if invoice exists
                cursor.execute("""
                    SELECT i.TOTAL_AMOUNT, i.STATUS, COALESCE(SUM(p.AMOUNT_PAID), 0) as PAID_AMOUNT
                    FROM INVOICE i
                    LEFT JOIN PAYMENT p ON i.INVOICE_ID = p.INVOICE_ID
                    WHERE i.INVOICE_ID = ?
                    GROUP BY i.INVOICE_ID, i.TOTAL_AMOUNT, i.STATUS
                """, (invoice_id,))

                invoice_info = cursor.fetchone()

                # If invoice not found, return error
                if not invoice_info:
                    log(f"Invoice {invoice_id} not found")
                    return False

                # Unpack invoice info
                total_amount, current_status, paid_amount = invoice_info
                # Calculate remaining amount
                remaining_amount = total_amount - paid_amount

                # Validate payment amount
                payment_amount = float(payment_data['AMOUNT_PAID'])

                # Check if payment amount is valid
                if payment_amount <= 0:
                    log(f"Invalid payment amount: {payment_amount}")
                    return False

                # Check if invoice is already fully paid
                if payment_amount > remaining_amount + 0.01:  # Allow small rounding differences
                    log(f"Payment amount ({payment_amount}) exceeds remaining balance ({remaining_amount})")
                    return False

                # Insert payment record
                cursor.execute("""
                    INSERT INTO PAYMENT (
                        INVOICE_ID, PAYMENT_DATE, AMOUNT_PAID, PAYMENT_METHOD,
                        TRANSACTION_ID, REFERENCE_NUMBER, NOTES, STATUS, PROCESSED_BY
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_id,
                    payment_data.get('PAYMENT_DATE', datetime.now().date()),
                    payment_amount,
                    payment_data['PAYMENT_METHOD'],
                    payment_data.get('TRANSACTION_ID'),
                    payment_data.get('REFERENCE_NUMBER'),
                    payment_data.get('NOTES'),
                    'Completed',
                    payment_data.get('PROCESSED_BY')
                ))
                new_paid_amount = paid_amount + payment_amount

                # Update invoice status based on new paid amount
                if new_paid_amount >= total_amount - 0.01:  # 0.01 for rounding errors
                    new_status = 'Paid'
                elif new_paid_amount > 0:
                    new_status = 'Partial'
                else:
                    new_status = 'Pending'

                cursor.execute("""
                    UPDATE INVOICE 
                    SET STATUS = ?, UPDATED_DATE = CURRENT_TIMESTAMP
                    WHERE INVOICE_ID = ?
                """, (new_status, invoice_id))

                conn.commit()

                log(f"Payment of ${payment_amount:.2f} processed for invoice {invoice_id}")
                log(f"Invoice status updated to: {new_status}")

                return True

        except Exception as e:
            log(f"Error processing payment: {str(e)}", "ERROR")
            return False


    # ROOM RATE
    def add_room_rate(self, room_type_id, rate_data):
        """Add a new room rate for a room type"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ROOM_RATE (
                        ROOM_TYPE_ID, RATE_NAME, BASE_RATE, EXTRA_ADULT_RATE, 
                        EXTRA_CHILD_RATE, EFFECTIVE_DATE, EXPIRY_DATE, IS_ACTIVE
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    room_type_id,
                    rate_data.get('RATE_NAME', 'Standard Rate'),
                    rate_data['BASE_RATE'],
                    rate_data.get('EXTRA_ADULT_RATE', 0.00),
                    rate_data.get('EXTRA_CHILD_RATE', 0.00),
                    rate_data['EFFECTIVE_DATE'],
                    rate_data.get('EXPIRY_DATE'),
                    rate_data.get('IS_ACTIVE', 1)
                ))
                conn.commit()
                log(f"Room rate added for room type {room_type_id}")
                return cursor.lastrowid
        except Exception as e:
            log(f"Error adding room rate: {str(e)}", "ERROR")
            return None


    def get_current_room_rate(self, room_type_id, check_date=None):
        """Get the current active room rate for a room type"""
        # when adding a new reservation, use get_current_room_rate to calculate the proper charges
        try:
            if not check_date:
                from datetime import date
                check_date = date.today()

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM ROOM_RATE 
                    WHERE ROOM_TYPE_ID = ? 
                    AND IS_ACTIVE = 1 
                    AND EFFECTIVE_DATE <= ?
                    AND (EXPIRY_DATE IS NULL OR EXPIRY_DATE >= ?)
                    ORDER BY EFFECTIVE_DATE DESC
                    LIMIT 1
                """, (room_type_id, check_date, check_date))

                return cursor.fetchone()
        except Exception as e:
            log(f"Error getting room rate: {str(e)}", "ERROR")
            return None


    def get_room_rate_by_room_type(self, room_type_id):
        """Get the existing rate for a room type (regardless of active status) - s"""
        # when editing room rates, use this to retrieve the existing rate configuration regardless if it's active.
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM ROOM_RATE 
                    WHERE ROOM_TYPE_ID = ?
                    ORDER BY CREATED_DATE DESC
                    LIMIT 1
                """, (room_type_id,))

                result = cursor.fetchone()
                if result:
                    # Convert to dictionary
                    columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                              "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                              "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            log(f"Error getting room rate by room type: {str(e)}", "ERROR")
            return None


    def update_room_rate(self, rate_id, rate_data):
        """Update an existing room rate"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE ROOM_RATE 
                    SET RATE_NAME = ?, BASE_RATE = ?, EXTRA_ADULT_RATE = ?,
                        EXTRA_CHILD_RATE = ?, EFFECTIVE_DATE = ?, EXPIRY_DATE = ?,
                        IS_ACTIVE = ?
                    WHERE RATE_ID = ?
                """, (
                    rate_data['RATE_NAME'],
                    rate_data['BASE_RATE'],
                    rate_data['EXTRA_ADULT_RATE'],
                    rate_data['EXTRA_CHILD_RATE'],
                    rate_data['EFFECTIVE_DATE'],
                    rate_data.get('EXPIRY_DATE'),
                    rate_data.get('IS_ACTIVE', 1),
                    rate_id
                ))
                conn.commit()
                log(f"Room rate {rate_id} updated successfully")
                return True
        except Exception as e:
            log(f"Error updating room rate: {str(e)}", "ERROR")
            return False


    def get_detailed_charge_breakdown(self, reservation_id):
        """Get detailed breakdown of all charges for the invoice popup's service table - s"""
        try:
            from models.reservation import ReservationModel
            from models.room import RoomModel

            reservation_model = ReservationModel()
            room_model = RoomModel()

            # Get reservation details
            reservation = reservation_model.get_reservation_by_id(reservation_id)
            # If reservation not found, return None
            if not reservation:
                return None

            # Get room data
            room_id = reservation.get("ROOM_ID")
            room_data = room_model.get_room_data_with_type(room_id)
            # If room data not found, return None
            if not room_data:
                return None

            # Calculate nights - s
            check_in_date = datetime.strptime(reservation.get("CHECK_IN_DATE"), "%Y-%m-%d")
            check_out_date = datetime.strptime(reservation.get("CHECK_OUT_DATE"), "%Y-%m-%d")
            nights = (check_out_date - check_in_date).days

            if nights <= 0:
                nights = 1

            # Get room rate and guest details - s
            room_type_id = room_data.get('ROOM_TYPE_ID')
            base_rate = self.get_room_rate(room_type_id)

            if base_rate is None:
                return None

            num_adults = reservation.get("NUMBER_OF_ADULTS", 1)
            num_children = reservation.get("NUMBER_OF_CHILDREN", 0)

            # Build detailed line items
            line_items = []

            # 1. Base room accommodation
            room_type_name = room_data.get('TYPE_NAME', 'Standard Room')
            room_number = room_data.get('ROOM_NUMBER', 'N/A')
            base_total = nights * base_rate

            line_items.append({
                'description': f"Room Accommodation - {room_number} ({room_type_name})",
                'quantity': nights,
                'unit_price': base_rate,
                'total_price': base_total,
                'category': 'accommodation'
            })

            # 2. Extra guest charges
            room_type = room_model.get_room_type_by_id(room_type_id)
            if room_type:
                base_adults = room_type.get('BASE_ADULT_NUM', 2)
                base_children = room_type.get('BASE_CHILD_NUM', 0)

                extra_adults = max(0, num_adults - base_adults)
                extra_children = max(0, num_children - base_children)

                # Extra adult charges
                if extra_adults > 0:
                    # Get rates from room type or current room rate
                    current_rate = self.get_current_room_rate(room_type_id)
                    extra_adult_rate = room_type.get('EXTRA_ADULT_RATE', 0)

                    if current_rate:
                        columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                                  "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                                  "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                        rate_dict = dict(zip(columns, current_rate))

                        if rate_dict['EXTRA_ADULT_RATE'] > 0:
                            extra_adult_rate = float(rate_dict['EXTRA_ADULT_RATE'])

                    if extra_adult_rate == 0:
                        extra_adult_rate = float(self.settings_model.get_billing_setting('DEFAULT_EXTRA_ADULT_RATE', 0.0))

                    extra_adult_total = extra_adults * extra_adult_rate * nights

                    if extra_adult_total > 0:
                        line_items.append({
                            'description': f"Extra Adult Fee ({extra_adults} adult{'s' if extra_adults > 1 else ''})",
                            'quantity': extra_adults * nights,
                            'unit_price': extra_adult_rate,
                            'total_price': extra_adult_total,
                            'category': 'extra_guests'
                        })

                # Extra children charges
                if extra_children > 0:
                    # Get rates from room type or current room rate
                    current_rate = self.get_current_room_rate(room_type_id) if not 'current_rate' in locals() else current_rate
                    extra_child_rate = room_type.get('EXTRA_CHILD_RATE', 0)

                    if current_rate:
                        if not 'rate_dict' in locals():
                            columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                                      "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                                      "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                            rate_dict = dict(zip(columns, current_rate))

                        if rate_dict['EXTRA_CHILD_RATE'] > 0:
                            extra_child_rate = float(rate_dict['EXTRA_CHILD_RATE'])

                    if extra_child_rate == 0:
                        extra_child_rate = float(self.settings_model.get_billing_setting('DEFAULT_EXTRA_CHILD_RATE', 0.0))

                    extra_child_total = extra_children * extra_child_rate * nights

                    if extra_child_total > 0:
                        line_items.append({
                            'description': f"Extra Child Fee ({extra_children} child{'ren' if extra_children > 1 else ''})",
                            'quantity': extra_children * nights,
                            'unit_price': extra_child_rate,
                            'total_price': extra_child_total,
                            'category': 'extra_guests'
                        })

            # 3. Time-based fees (early check-in, late checkout)
            time_based_fees = self.calculate_time_based_fees(reservation)
            if time_based_fees > 0:
                notes = reservation.get("NOTES", "").lower()

                if "early check" in notes or "early arrival" in notes:
                    early_checkin_fee = self.settings_model.get_billing_setting('EARLY_CHECKIN_FEE', 25.0)
                    if early_checkin_fee > 0:
                        line_items.append({
                            'description': "Early Check-in Fee",
                            'quantity': 1,
                            'unit_price': early_checkin_fee,
                            'total_price': early_checkin_fee,
                            'category': 'time_fees'
                        })

                if "late check" in notes or "late departure" in notes:
                    late_checkout_fee = self.settings_model.get_billing_setting('LATE_CHECKOUT_FEE', 50.0)
                    if late_checkout_fee > 0:
                        line_items.append({
                            'description': "Late Check-out Fee",
                            'quantity': 1,
                            'unit_price': late_checkout_fee,
                            'total_price': late_checkout_fee,
                            'category': 'time_fees'
                        })

            # Calculate subtotal before service charge
            charges_before_service = sum(item['total_price'] for item in line_items)

            # 4. Apply service charge
            service_charge_rate = self.get_service_charge_rate()
            if service_charge_rate > 0:
                service_charge = charges_before_service * service_charge_rate
                if service_charge > 0:
                    line_items.append({
                        'description': f"Service Charge ({int(service_charge_rate * 100)}%)",
                        'quantity': 1,
                        'unit_price': service_charge,
                        'total_price': service_charge,
                        'category': 'service_charge'
                    })

            # 5. Calculate final subtotal
            subtotal = sum(item['total_price'] for item in line_items)

            # Return structured data for the invoice
            return {
                'reservation_id': reservation_id,
                'line_items': line_items,
                'subtotal': subtotal,
                'room_id': room_id,
                'room_number': room_number,
                'room_type': room_type_name,
                'nights': nights
            }

        except Exception as e:
            log(f"Error getting detailed charge breakdown: {str(e)}", "ERROR")
            return None


    def is_reservation_paid(self, reservation_id):
        """Check if a reservation is fully paid based on its invoice,
        used when editing reservations to prevent editing when paid"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Get the invoice for this reservation
                cursor.execute("""
                    SELECT INVOICE_ID, TOTAL_AMOUNT, STATUS 
                    FROM INVOICE 
                    WHERE RESERVATION_ID = ?
                """, (reservation_id,))

                invoice = cursor.fetchone()
                # If no invoice exists, consider it unpaid
                if not invoice:
                    return False

                invoice_id, total_amount, status = invoice

                # If invoice status is 'Paid', it's already considered paid
                if status == 'Paid':
                    return True

                # Check total payment amount
                cursor.execute("""
                    SELECT SUM(AMOUNT_PAID) 
                    FROM PAYMENT 
                    WHERE INVOICE_ID = ? AND STATUS = 'Completed'
                """, (invoice_id,))

                total_paid = cursor.fetchone()[0] or 0

                # Consider it paid if payment equals or exceeds the total amount
                return total_paid >= total_amount

        except Exception as e:
            log(f"Error checking if reservation is paid: {str(e)}", "ERROR")
            return False


    def process_refund(self, reservation_id, refund_data):
        """Process a refund for a reservation's invoice"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Get the invoice for this reservation
                cursor.execute("""
                    SELECT INVOICE_ID, TOTAL_AMOUNT
                    FROM INVOICE
                    WHERE RESERVATION_ID = ?
                """, (reservation_id,))

                invoice_result = cursor.fetchone()

                # If no invoice exists, we cannot process a refund
                if not invoice_result:
                    log(f"No invoice found for reservation {reservation_id}", "ERROR")
                    return False

                invoice_id, total_amount = invoice_result

                # Get the payments for this invoice
                cursor.execute("""
                    SELECT PAYMENT_ID, AMOUNT_PAID, PAYMENT_METHOD
                    FROM PAYMENT
                    WHERE INVOICE_ID = ? AND STATUS = 'Completed'
                    ORDER BY PAYMENT_DATE DESC
                """, (invoice_id,))

                payments = cursor.fetchall()
                # If no payments found, we cannot process a refund
                if not payments:
                    log(f"No payments found for invoice {invoice_id}", "ERROR")
                    return False

                # Get the most recent payment
                payment_id, amount_paid, payment_method = payments[0]

                # Validate refund amount
                refund_amount = float(refund_data.get('AMOUNT_REFUNDED', 0))
                if refund_amount <= 0:
                    log("Refund amount must be positive", "ERROR")
                    return False
                if refund_amount > amount_paid:
                    log(f"Refund amount {refund_amount} exceeds payment amount {amount_paid}", "ERROR")
                    return False

                refund_notes = refund_data.get('NOTES', 'Refund for reservation cancellation')
                refund_method = refund_data.get('REFUND_METHOD', payment_method)

                # Insert refund payment record
                cursor.execute("""
                    INSERT INTO PAYMENT (
                        INVOICE_ID, PAYMENT_DATE, AMOUNT_PAID, PAYMENT_METHOD,
                        TRANSACTION_ID, REFERENCE_NUMBER, STATUS, NOTES
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_id,
                    datetime.now().date(),
                    -refund_amount,  # Negative amount indicates a refund
                    f"Refund via {refund_method}",
                    refund_data.get('TRANSACTION_ID'),
                    None,
                    'Refunded',
                    refund_notes
                ))

                # Update the original payment record to indicate it was refunded
                cursor.execute("""
                    UPDATE PAYMENT
                    SET STATUS = 'Refunded', 
                        NOTES = COALESCE(NOTES, '') || ' | Refunded: ' || ?
                    WHERE PAYMENT_ID = ?
                """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), payment_id))

                # Update the invoice status based on total payments
                cursor.execute("""
                    SELECT SUM(AMOUNT_PAID) as TOTAL_PAID
                    FROM PAYMENT
                    WHERE INVOICE_ID = ?
                """, (invoice_id,))

                total_paid = cursor.fetchone()[0] or 0

                # Determine new invoice status based on total paid
                if total_paid <= 0:
                    new_status = 'Refunded'
                elif total_paid < total_amount:
                    new_status = 'Partial'
                else:
                    new_status = 'Paid'

                # Update the invoice status
                cursor.execute("""
                    UPDATE INVOICE
                    SET STATUS = ?, UPDATED_DATE = CURRENT_TIMESTAMP
                    WHERE INVOICE_ID = ?
                """, (new_status, invoice_id))

                conn.commit()
                log(f"Refund of {refund_amount} processed successfully for invoice {invoice_id}", "INFO")
                return True

        except Exception as e:
            log(f"Error processing refund: {str(e)}", "ERROR")
            return False


    def check_payment_status_for_reservation(self, reservation_id):
        """Check if a reservation has payments that may need to be refunded before cancellation of reservation"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Get invoice for this reservation
                cursor.execute("""
                    SELECT i.INVOICE_ID, i.TOTAL_AMOUNT, i.STATUS,
                           COALESCE(SUM(CASE WHEN p.STATUS != 'Refunded' THEN p.AMOUNT_PAID ELSE 0 END), 0) as AMOUNT_PAID
                    FROM INVOICE i
                    LEFT JOIN PAYMENT p ON i.INVOICE_ID = p.INVOICE_ID
                    WHERE i.RESERVATION_ID = ?
                    GROUP BY i.INVOICE_ID
                """, (reservation_id,))

                result = cursor.fetchone()

                # If no invoice found, return default values
                if not result:
                    return {'has_payments': False, 'needs_refund': False, 'amount': 0.0}

                invoice_id, total_amount, status, amount_paid = result

                return {
                    'has_payments': amount_paid > 0,
                    'needs_refund': amount_paid > 0,
                    'amount': amount_paid,
                    'invoice_id': invoice_id,
                    'status': status
                }

        except Exception as e:
            log(f"Error checking payment status: {str(e)}", "ERROR")
            return {'has_payments': False, 'needs_refund': False, 'amount': 0.0}

