import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

from models.guest import GuestModel
from models.reservation import ReservationModel
from models.room import RoomModel
from models.billing import BillingModel
from models.hotel import HotelModel
from utils.helpers import log


class BillingInvoicePage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"

    def __init__(self, master=None, invoice_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=self.BG_COLOR_2)
        self.pack(fill="both", expand=True)

        self.invoice_data = invoice_data
        self.hotel_model = HotelModel()
        self.guest_model = GuestModel()
        self.reservation_model = ReservationModel()
        self.room_model = RoomModel()
        self.billing_model = BillingModel()

        # Set window size
        if master:
            master.geometry("1000x800")

        self.create_widgets()

        if self.invoice_data:
            self.populate_invoice_fields(self.invoice_data)

    def create_widgets(self):
        # Main Invoice Frame with padding - remove right padding to let scrollbar go to edge
        self.invoice_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BG_COLOR_2,
            corner_radius=0,
            scrollbar_button_color="#E0E0E0",  # Make scrollbar less visible
            scrollbar_button_hover_color="#C0C0C0"
        )
        self.invoice_frame.pack(fill="both", expand=True, padx=(20, 0), pady=20)  # Remove right padding

        # Create inner content frame with proper padding
        content_wrapper = ctk.CTkFrame(self.invoice_frame, fg_color=self.BG_COLOR_2, corner_radius=0)
        content_wrapper.pack(fill="both", expand=True, padx=(0, 20))  # Add right padding here instead

        # Header Section
        header_frame = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        # Hotel Information (Left side)
        hotel_info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        hotel_info_frame.pack(side="left", anchor="nw")

        # Get hotel information from database
        try:
            hotel_info = self.hotel_model.get_hotel_info(1)  # Assuming hotel ID 1 is the default
            if hotel_info:
                hotel_name = hotel_info.get('HOTEL_NAME', 'Reverie Hotel')
                hotel_address = hotel_info.get('ADDRESS', '123 Main Street, City, Country')
                hotel_phone = hotel_info.get('PHONE_NUMBER', '+1 234 567 8900')
                hotel_email = hotel_info.get('EMAIL', 'reverie@hotel.com')
            else:
                # Fallback to default values if no hotel info found
                hotel_name = 'GRAND HOTEL'
                hotel_address = '123 Main Street, City, Country'
                hotel_phone = '+1 234 567 8900'
                hotel_email = 'billing@grandhotel.com'
        except Exception as e:
            log(f"Error getting hotel info: {str(e)}", "WARNING")
            # Fallback to default values
            hotel_name = 'GRAND HOTEL'
            hotel_address = '123 Main Street, City, Country'
            hotel_phone = '+1 234 567 8900'
            hotel_email = 'billing@grandhotel.com'

        ctk.CTkLabel(hotel_info_frame, text=hotel_name.upper(),
                    font=("Roboto Condensed", 24, "bold"),
                    text_color="#2563eb").pack(anchor="w")
        ctk.CTkLabel(hotel_info_frame, text=hotel_address,
                    font=("Roboto", 12), text_color="#666").pack(anchor="w")
        ctk.CTkLabel(hotel_info_frame, text=f"Phone: {hotel_phone}",
                    font=("Roboto", 12), text_color="#666").pack(anchor="w")
        ctk.CTkLabel(hotel_info_frame, text=f"Email: {hotel_email}",
                    font=("Roboto", 12), text_color="#666").pack(anchor="w")

        # Invoice Title and Number (Right side)
        invoice_header_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        invoice_header_frame.pack(side="right", anchor="ne")

        ctk.CTkLabel(invoice_header_frame, text="INVOICE",
                    font=("Roboto Condensed", 28, "bold"),
                    text_color=self.TITLE_COLOR).pack(anchor="e")

        self.invoice_number_label = ctk.CTkLabel(invoice_header_frame, text="Invoice #: INV0000",
                                                font=("Roboto", 14, "bold"),
                                                text_color="#666")
        self.invoice_number_label.pack(anchor="e")

        self.invoice_date_label = ctk.CTkLabel(invoice_header_frame,
                                              text=f"Date: {datetime.now().strftime('%B %d, %Y')}",
                                              font=("Roboto", 12), text_color="#666")
        self.invoice_date_label.pack(anchor="e")

        # Divider
        divider1 = ctk.CTkFrame(content_wrapper, fg_color="#e5e7eb", height=2)
        divider1.pack(fill="x", pady=20)

        # Guest and Booking Info Row
        info_section = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        info_section.pack(fill="x", pady=(0, 20))

        # Guest Information
        guest_frame = ctk.CTkFrame(info_section, fg_color=self.BG_COLOR_1, corner_radius=8)
        guest_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(guest_frame, text="BILL TO:",
                    font=("Roboto Condensed", 14, "bold"),
                    text_color=self.TITLE_COLOR).pack(anchor="nw", padx=15, pady=(15, 5))

        self.guest_name_label = ctk.CTkLabel(guest_frame, text="Guest Name: -",
                                           font=("Roboto", 12, "bold"),
                                           text_color="#333", anchor="w")
        self.guest_name_label.pack(anchor="nw", padx=15, pady=2)

        self.guest_email_label = ctk.CTkLabel(guest_frame, text="Email: -",
                                            font=("Roboto", 11),
                                            text_color="#666", anchor="w")
        self.guest_email_label.pack(anchor="nw", padx=15, pady=1)

        self.guest_contact_label = ctk.CTkLabel(guest_frame, text="Contact: -",
                                              font=("Roboto", 11),
                                              text_color="#666", anchor="w")
        self.guest_contact_label.pack(anchor="nw", padx=15, pady=(1, 15))

        # Booking Information
        booking_frame = ctk.CTkFrame(info_section, fg_color=self.BG_COLOR_1, corner_radius=8)
        booking_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(booking_frame, text="BOOKING DETAILS:",
                    font=("Roboto Condensed", 14, "bold"),
                    text_color=self.TITLE_COLOR).pack(anchor="nw", padx=15, pady=(15, 5))

        self.reservation_id_label = ctk.CTkLabel(booking_frame, text="Reservation: -",
                                               font=("Roboto", 12, "bold"),
                                               text_color="#333", anchor="w")
        self.reservation_id_label.pack(anchor="nw", padx=15, pady=2)

        self.room_info_label = ctk.CTkLabel(booking_frame, text="Room: -",
                                          font=("Roboto", 11),
                                          text_color="#666", anchor="w")
        self.room_info_label.pack(anchor="nw", padx=15, pady=1)

        self.dates_label = ctk.CTkLabel(booking_frame, text="Dates: -",
                                      font=("Roboto", 11),
                                      text_color="#666", anchor="w")
        self.dates_label.pack(anchor="nw", padx=15, pady=1)

        self.nights_label = ctk.CTkLabel(booking_frame, text="Nights: -",
                                       font=("Roboto", 11),
                                       text_color="#666", anchor="w")
        self.nights_label.pack(anchor="nw", padx=15, pady=(1, 15))

        # Services Table
        services_frame = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        services_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(services_frame, text="SERVICES & CHARGES",
                    font=("Roboto Condensed", 16, "bold"),
                    text_color=self.TITLE_COLOR).pack(anchor="w", pady=(0, 10))

        # Create treeview for services
        columns = ("Description", "Qty", "Amount")

        style = ttk.Style()
        style.configure("Invoice.Treeview.Heading",
                       font=("Roboto Condensed", 12, "bold"),
                       foreground="#333")
        style.configure("Invoice.Treeview",
                       font=("Roboto", 11),
                       rowheight=30)

        self.services_tree = ttk.Treeview(services_frame,
                                         columns=columns,
                                         show="headings",
                                         height=6,
                                         style="Invoice.Treeview")

        # Configure columns
        self.services_tree.heading("Description", text="Description", anchor="w")
        self.services_tree.heading("Qty", text="Qty", anchor="center")
        self.services_tree.heading("Amount", text="Amount", anchor="e")

        self.services_tree.column("Description", width=400, anchor="w")
        self.services_tree.column("Qty", width=80, anchor="center")
        self.services_tree.column("Amount", width=150, anchor="e")

        self.services_tree.pack(fill="x", pady=(0, 10))

        # Configure row colors
        self.services_tree.tag_configure('oddrow', background='#f8f9fa')
        self.services_tree.tag_configure('evenrow', background='white')

        # Summary Section
        summary_container = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        summary_container.pack(fill="x", pady=(10, 20))

        # Empty space on left
        ctk.CTkFrame(summary_container, fg_color="transparent", width=400).pack(side="left")

        # Summary on right
        summary_frame = ctk.CTkFrame(summary_container, fg_color=self.BG_COLOR_1, corner_radius=8)
        summary_frame.pack(side="right", padx=(20, 0))

        # Summary content
        summary_content = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_content.pack(padx=20, pady=15)

        # Summary rows
        self.subtotal_label = ctk.CTkLabel(summary_content, text="Subtotal: ₱0.00",
                                         font=("Roboto", 12), text_color="#666")
        self.subtotal_label.grid(row=0, column=0, sticky="e", padx=(0, 40), pady=2)

        self.tax_label = ctk.CTkLabel(summary_content, text="Tax (12%): ₱0.00",
                                    font=("Roboto", 12), text_color="#666")
        self.tax_label.grid(row=1, column=0, sticky="e", padx=(0, 40), pady=2)

        # Divider in summary
        summary_divider = ctk.CTkFrame(summary_content, fg_color="#ccc", height=1)
        summary_divider.grid(row=2, column=0, sticky="ew", padx=(0, 40), pady=(5, 5))

        self.total_label = ctk.CTkLabel(summary_content, text="TOTAL: ₱0.00",
                                      font=("Roboto", 14, "bold"), text_color="#333")
        self.total_label.grid(row=3, column=0, sticky="e", padx=(0, 40), pady=2)

        self.payment_status_label = ctk.CTkLabel(summary_content, text="Status: Pending",
                                               font=("Roboto", 12, "bold"), text_color="#dc3545")
        self.payment_status_label.grid(row=4, column=0, sticky="e", padx=(0, 40), pady=(5, 0))

        # Payment Information (if paid)
        self.payment_info_frame = ctk.CTkFrame(content_wrapper, fg_color=self.BG_COLOR_1, corner_radius=8)
        self.payment_method_label = ctk.CTkLabel(self.payment_info_frame, text="Payment Method: -",
                                               font=("Roboto", 11), text_color="#666")
        self.payment_date_label = ctk.CTkLabel(self.payment_info_frame, text="Payment Date: -",
                                             font=("Roboto", 11), text_color="#666")

        # Footer
        footer_frame = ctk.CTkFrame(content_wrapper, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))

        # Notes
        notes_frame = ctk.CTkFrame(footer_frame, fg_color=self.BG_COLOR_1, corner_radius=8)
        notes_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(notes_frame, text="NOTES:",
                    font=("Roboto Condensed", 12, "bold"),
                    text_color=self.TITLE_COLOR).pack(anchor="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(notes_frame,
                    text="Thank you for choosing Grand Hotel. We hope you enjoyed your stay!",
                    font=("Roboto", 11, "italic"),
                    text_color="#666", wraplength=700).pack(anchor="w", padx=15, pady=(0, 10))

        # Action Buttons
        button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        # Print/Download button
        self.download_button = ctk.CTkButton(button_frame, text="Download PDF",
                                           font=("Roboto Condensed", 14, "bold"),
                                           width=150, height=40,
                                           fg_color="#2563eb", hover_color="#1d4ed8",
                                           command=self.download_invoice)
        self.download_button.pack(side="right", padx=(10, 0))

        # Print button
        self.print_button = ctk.CTkButton(button_frame, text="Print Invoice",
                                        font=("Roboto Condensed", 14, "bold"),
                                        width=150, height=40,
                                        fg_color="#28a745", hover_color="#218838",
                                        command=self.print_invoice)
        self.print_button.pack(side="right", padx=(10, 0))

        # Close button
        self.close_button = ctk.CTkButton(button_frame, text="Close",
                                        font=("Roboto Condensed", 14, "bold"),
                                        width=100, height=40,
                                        fg_color="#6c757d", hover_color="#545b62",
                                        command=self.close_window)
        self.close_button.pack(side="right")

    def populate_invoice_fields(self, billing_data):
        """Populate invoice with billing data from the billing page"""
        try:
            # billing_data format: (invoice_id, reservation_id, guest_name, room_number, check_in, check_out, amount, payment_status)
            invoice_id_display, reservation_id_str, guest_name, room_number, check_in, check_out, amount_str, payment_status = billing_data

            # Update header information
            self.invoice_number_label.configure(text=f"Invoice #: {invoice_id_display}")

            # Get reservation ID as integer
            reservation_id = int(reservation_id_str[1:]) if reservation_id_str.startswith("R") else None

            if not reservation_id:
                messagebox.showerror("Error", "Invalid reservation ID format.")
                return

            # Get detailed invoice information from billing model
            detailed_invoice = self.billing_model.get_invoice_by_reservation(reservation_id)

            # Populate invoice with the best available data
            self.populate_invoice_content(reservation_id, detailed_invoice, billing_data)

        except Exception as e:
            log(f"Error populating invoice: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not load invoice details: {str(e)}")

    def populate_invoice_content(self, reservation_id, detailed_invoice=None, billing_data=None):
        """Populate invoice using the best available data sources"""
        try:
            # Start with reservation data (always required)
            reservation = self.reservation_model.get_reservation_by_id(reservation_id)
            if not reservation:
                raise ValueError(f"Reservation R{reservation_id} not found")

            guest_id = reservation.get("GUEST_ID")
            room_id = reservation.get("ROOM_ID")

            # ---- GUEST INFORMATION ----
            guest = self.guest_model.get_guest_by_id(guest_id)
            if guest:
                self.guest_name_label.configure(text=f"Guest: {guest.get('FIRST_NAME', '')} {guest.get('LAST_NAME', '')}")
                self.guest_email_label.configure(text=f"Email: {guest.get('EMAIL', 'N/A')}")
                self.guest_contact_label.configure(text=f"Contact: {guest.get('CONTACT_NUMBER', 'N/A')}")

            # ---- ROOM INFORMATION ----
            room_data = self.room_model.get_room_data_with_type(room_id)
            room_type = "Standard"
            room_number = "N/A"

            if room_data:
                room_type = room_data.get('TYPE_NAME', 'Standard')
                room_number = room_data.get('ROOM_NUMBER', 'N/A')
            elif billing_data:
                room_number = billing_data[3]  # Use room number from billing data if available

            self.room_info_label.configure(text=f"Room: {room_number} ({room_type})")

            # ---- BOOKING DATES ----
            self.reservation_id_label.configure(text=f"Reservation: R{reservation_id}")

            # Use detailed_invoice dates if available, otherwise use billing_data
            check_in_date_str = None
            check_out_date_str = None

            if detailed_invoice:
                check_in_date_str = detailed_invoice.get('CHECK_IN_DATE')
                check_out_date_str = detailed_invoice.get('CHECK_OUT_DATE')
            elif billing_data:
                check_in_date_str = billing_data[4]
                check_out_date_str = billing_data[5]

            # If we have both dates, update the UI and calculate nights
            if check_in_date_str and check_out_date_str:
                self.dates_label.configure(text=f"Dates: {check_in_date_str} to {check_out_date_str}")

                # Calculate nights
                try:
                    check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d")
                    check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d")
                    nights = (check_out_date - check_in_date).days
                    if nights <= 0:
                        nights = 1
                    self.nights_label.configure(text=f"Nights: {nights}")
                except:
                    nights = 1
                    self.nights_label.configure(text="Nights: 1")

            # ---- SERVICES & CHARGES ----
            if detailed_invoice:
                # Try to get detailed breakdown
                self.populate_services_table_from_detail(detailed_invoice, nights if 'nights' in locals() else 1)
            else:
                # Use basic calculation with billing_data
                self.populate_services_table_basic(billing_data, nights if 'nights' in locals() else 1)

            # ---- PAYMENT STATUS ----
            if detailed_invoice:
                self.update_payment_status_detailed(detailed_invoice)
            elif billing_data:
                self.update_payment_status(billing_data[7])
            else:
                self.update_payment_status("Pending")

        except Exception as e:
            log(f"Error populating invoice content: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not populate invoice content: {str(e)}")

    def populate_services_table_from_detail(self, detailed_invoice, nights=1):
        """Populate the services table with detailed billing items"""
        # Clear existing items
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)

        try:
            # Get detailed charge breakdown from billing model
            reservation_id = detailed_invoice['RESERVATION_ID']
            charge_breakdown = self.billing_model.get_detailed_charge_breakdown(reservation_id)

            if charge_breakdown and charge_breakdown.get('line_items'):
                # Use the detailed breakdown
                line_items = charge_breakdown['line_items']

                for i, item in enumerate(line_items):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    self.services_tree.insert("", "end",
                                            values=(
                                                item['description'],
                                                item['quantity'],
                                                f"₱{float(item['total_price']):.2f}"
                                            ),
                                            tags=(tag,))

                # Calculate totals correctly including service charge in subtotal
                subtotal = sum(float(item['total_price']) for item in line_items)

                # Calculate tax on the full subtotal (including service charges)
                tax_rate = float(detailed_invoice.get('TAX_RATE', 0.12))
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount

                # Update summary
                self.subtotal_label.configure(text=f"Subtotal: ₱{subtotal:.2f}")
                self.tax_label.configure(text=f"Tax ({tax_rate*100:.0f}%): ₱{tax_amount:.2f}")
                self.total_label.configure(text=f"TOTAL: ₱{total_amount:.2f}")

            else:
                # Fallback to basic calculation if detailed breakdown fails
                self.populate_services_table_fallback(detailed_invoice, nights)

        except Exception as e:
            log(f"Error populating detailed services table: {str(e)}", "ERROR")
            # Fallback to basic calculation
            self.populate_services_table_fallback(detailed_invoice, nights)

    def populate_services_table_fallback(self, detailed_invoice, nights=1):
        """Fallback method for populating services when detailed breakdown fails"""
        try:
            # Clear existing items
            for item in self.services_tree.get_children():
                self.services_tree.delete(item)

            # Get room details
            room_id = detailed_invoice['ROOM_ID']
            room_data = self.room_model.get_room_data_with_type(room_id)

            if room_data:
                room_number = room_data.get('ROOM_NUMBER', 'N/A')
                room_type = room_data.get('TYPE_NAME', 'Standard Room')

                # Calculate base rate from subtotal
                subtotal = float(detailed_invoice['SUBTOTAL'])
                base_rate = subtotal / nights

                # Add basic room accommodation row
                self.services_tree.insert("", "end",
                                        values=(
                                            f"Room Accommodation - {room_number} ({room_type})",
                                            nights,
                                            f"₱{subtotal:.2f}"
                                        ),
                                        tags=('evenrow',))

            # Update summary with actual invoice totals
            subtotal = float(detailed_invoice['SUBTOTAL'])
            tax_amount = float(detailed_invoice['TAX_AMOUNT'])
            total_amount = float(detailed_invoice['TOTAL_AMOUNT'])

            self.subtotal_label.configure(text=f"Subtotal: ₱{subtotal:.2f}")
            self.tax_label.configure(text=f"Tax ({detailed_invoice['TAX_RATE']*100:.0f}%): ₱{tax_amount:.2f}")
            self.total_label.configure(text=f"TOTAL: ₱{total_amount:.2f}")

        except Exception as e:
            log(f"Error in fallback services population: {str(e)}", "ERROR")

    def populate_services_table_basic(self, billing_data, nights=1):
        """Populate services table with basic billing data"""
        try:
            # Clear existing items
            for item in self.services_tree.get_children():
                self.services_tree.delete(item)

            if not billing_data:
                return

            room_number = billing_data[3]
            total_amount_str = billing_data[6]

            # Extract numeric amount from total_amount_str (e.g., "₱450.00" -> 450.00)
            if total_amount_str.startswith('₱'):
                total_amount_str = total_amount_str[1:]
            try:
                total_amount = float(total_amount_str)
            except ValueError:
                total_amount = 0.0

            # Calculate subtotal and tax
            tax_rate = 0.12  # Default tax rate
            subtotal = total_amount / (1 + tax_rate)
            tax_amount = total_amount - subtotal

            # Add basic room accommodation row
            self.services_tree.insert("", "end",
                                    values=(
                                        f"Room Accommodation - {room_number}",
                                        nights,
                                        f"₱{subtotal:.2f}"
                                    ),
                                    tags=('evenrow',))

            # Update summary
            self.subtotal_label.configure(text=f"Subtotal: ₱{subtotal:.2f}")
            self.tax_label.configure(text=f"Tax ({tax_rate*100:.0f}%): ₱{tax_amount:.2f}")
            self.total_label.configure(text=f"TOTAL: ₱{total_amount:.2f}")

        except Exception as e:
            log(f"Error populating basic services table: {str(e)}", "ERROR")

    def update_payment_status_detailed(self, detailed_invoice):
        """Update payment status using detailed invoice data"""
        try:
            payment_status = detailed_invoice['STATUS']
            status_colors = {
                "Paid": "#28a745",
                "Pending": "#ffc107",
                "Partial": "#fd7e14",
                "Overdue": "#dc3545",
                "Cancelled": "#6c757d"
            }

            color = status_colors.get(payment_status, "#6c757d")
            self.payment_status_label.configure(text=f"Status: {payment_status}", text_color=color)

            # Show payment info if there are payments
            payments = detailed_invoice.get('PAYMENTS', [])
            if payments:
                self.payment_info_frame.pack(fill="x", pady=(0, 15))
                self.payment_method_label.pack(anchor="w", padx=15, pady=(10, 2))
                self.payment_date_label.pack(anchor="w", padx=15, pady=(0, 10))

                # Show latest payment info
                latest_payment = payments[-1]  # Get most recent payment
                self.payment_method_label.configure(text=f"Payment Method: {latest_payment['PAYMENT_METHOD']}")
                self.payment_date_label.configure(text=f"Payment Date: {latest_payment['PAYMENT_DATE']}")

        except Exception as e:
            log(f"Error updating detailed payment status: {str(e)}", "ERROR")
            # Fallback to basic status update
            self.update_payment_status(detailed_invoice.get('STATUS', 'Pending'))

    def update_payment_status(self, status):
        """Update payment status display with basic status information"""
        try:
            status_colors = {
                "Paid": "#28a745",
                "Pending": "#ffc107",
                "Partial": "#fd7e14",
                "Overdue": "#dc3545",
                "Cancelled": "#6c757d"
            }

            color = status_colors.get(status, "#6c757d")
            self.payment_status_label.configure(text=f"Status: {status}", text_color=color)

            # Hide payment info frame for basic display unless it's paid
            if status == "Paid":
                # We don't have payment details here, so just show placeholder
                self.payment_info_frame.pack(fill="x", pady=(0, 15))
                self.payment_method_label.pack(anchor="w", padx=15, pady=(10, 2))
                self.payment_date_label.pack(anchor="w", padx=15, pady=(0, 10))
                self.payment_method_label.configure(text="Payment Method: Card/Cash")
                self.payment_date_label.configure(text="Payment Date: Recent")
            else:
                # Hide payment info for other statuses
                self.payment_info_frame.pack_forget()

        except Exception as e:
            log(f"Error updating payment status: {str(e)}", "ERROR")
            # Set a default value
            self.payment_status_label.configure(text="Status: Unknown", text_color="#6c757d")

    def download_invoice(self):
        """Download invoice as PDF"""
        messagebox.showinfo("Download", "Invoice download functionality will be implemented.")

    def print_invoice(self):
        """Print the invoice"""
        messagebox.showinfo("Print", "Invoice print functionality will be implemented.")

    def close_window(self):
        """Close the invoice window"""
        if self.master:
            self.master.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Invoice")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Sample data for testing
    sample_data = ("INV0001", "R1", "John Doe", "101", "2024-01-15", "2024-01-18", "₱450.00", "Paid")

    invoice_page = BillingInvoicePage(master=root, invoice_data=sample_data)
    root.mainloop()
