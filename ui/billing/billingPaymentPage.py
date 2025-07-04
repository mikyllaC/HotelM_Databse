import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar
from datetime import datetime

from models.guest import GuestModel
from models.reservation import ReservationModel
from models.room import RoomModel
from models.billing import BillingModel
from utils.helpers import log


class BillingPaymentPage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)
    TREE_SELECT_COLOR = "#DEECF7"

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.guest_model = GuestModel()
        self.reservation_model = ReservationModel()
        self.room_model = RoomModel()
        self.billing_model = BillingModel()

        # Updated column headers for the billing table
        self.billing_data = [
            ["Invoice ID", "Reservation ID", "Guest Name", "Room Number", "Check In", "Check Out", "Amount", "Payment Status"]
        ]

        self.create_widgets()
        self.populate_billing_records()

    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Billing Management", font=("Roboto Condensed", 28, "bold"),
                                   text_color=self.TITLE_COLOR)
        title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))

        # Action Bar Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(anchor="n", padx=(35, 0), fill="x")

        # Process Payment Button
        process_payment_button = ctk.CTkButton(
            self.action_frame,
            text="Process Payment",
            font=("Roboto Condensed", 16, "bold"),
            width=180,
            height=36,
            command=self.process_payment_popup,
            fg_color="#28a745",
            hover_color="#218838"
        )
        process_payment_button.pack(side="left", padx=(0, 10))

        # Process Refund Button
        process_refund_button = ctk.CTkButton(
            self.action_frame,
            text="Process Refund",
            font=("Roboto Condensed", 16, "bold"),
            width=180,
            height=36,
            command=self.process_refund_popup,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        process_refund_button.pack(side="left", padx=(0, 10))

        # Search Entry with auto-filter
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.filter_table())
        self.search_entry = ctk.CTkEntry(
            self.action_frame,
            width=220,
            height=36,
            placeholder_text="Search guest name or invoice...",
            textvariable=self.search_var,
            font=("Roboto Condensed", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.action_frame,
            width=160,
            height=36,
            values=["All Status", "Pending", "Paid", "Overdue", "Cancelled"],
            variable=self.filter_var,
            font=("Roboto Condensed", 14),
            command=lambda x: self.filter_table()
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(15, 10), fill="both", expand=True, anchor="n")

        # Right Frame for billing details
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        # Initially hidden
        self.right_frame.place_forget()

        # Treeview for displaying billing records
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=35, font=self.TREE_FONT, anchor="w")
        style.map("Treeview",
                  background=[('selected', self.TREE_SELECT_COLOR)],
                  foreground=[('selected', "black")])

        self.treeview = ttk.Treeview(self.table_frame, columns=self.billing_data[0], show="headings")
        self.treeview.pack(expand=True, fill="both")
        self.treeview.tag_configure('oddrow', background='#f5f5f5')
        self.treeview.tag_configure('evenrow', background='white')
        self.treeview.tag_configure('paid', background='#d4edda')
        self.treeview.tag_configure('pending', background='#fff3cd')
        self.treeview.tag_configure('overdue', background='#f8d7da')

        # Set column headings and widths
        for col in self.billing_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w", width=100, stretch=True)

        # Customize column widths
        self.treeview.column("Invoice ID", width=100, anchor="w")
        self.treeview.column("Reservation ID", width=120, anchor="w")
        self.treeview.column("Guest Name", width=150, anchor="w")
        self.treeview.column("Room Number", width=100, anchor="w")
        self.treeview.column("Check In", width=100, anchor="w")
        self.treeview.column("Check Out", width=100, anchor="w")
        self.treeview.column("Amount", width=120, anchor="w")
        self.treeview.column("Payment Status", width=120, anchor="w")

        # Bind row selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

    def populate_billing_records(self):
        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        try:
            # Get all reservations and create billing records using the billing model
            reservations = self.reservation_model.get_all_reservations()

            if not reservations:
                log("No reservations found for billing")
                self.treeview.insert("", "end", values=("-", "-", "-", "-", "-", "-", "-", "-"))
                return

            # For each reservation, get or auto-generate billing summary
            for i, reservation in enumerate(reservations):
                reservation_id = reservation.get("RESERVATION_ID")
                guest_id = reservation.get("GUEST_ID")
                room_id = reservation.get("ROOM_ID")

                guest_name = "Unknown Guest"
                room_number = "N/A"

                # Get guest details
                try:
                    guest = self.guest_model.get_guest_by_id(guest_id)
                    if guest:
                        guest_name = f"{guest.get('FIRST_NAME', 'Guest')} {guest.get('LAST_NAME', '')}"
                except Exception as e:
                    log(f"Could not get guest details for ID {guest_id}: {str(e)}", "WARNING")

                # Get room details
                try:
                    room_data = self.room_model.get_room_data_with_type(room_id)
                    if room_data:
                        room_number = room_data.get('ROOM_NUMBER', 'N/A')
                except Exception as e:
                    log(f"Could not get room details for ID {room_id}: {str(e)}", "WARNING")

                # Get billing summary from billing model (auto-generates if needed)
                billing_summary = self.billing_model.get_billing_summary_by_reservation(reservation_id)

                if billing_summary:
                    invoice_id = billing_summary['invoice_id']
                    total_amount = billing_summary['total_amount']
                    payment_status = billing_summary['payment_status']
                else:
                    # This should not happen with auto-generation, but fallback just in case
                    log(f"Could not get or generate billing summary for reservation {reservation_id}", "WARNING")
                    continue  # Skip this reservation instead of showing incomplete data

                # Format dates for display
                check_in_date = reservation.get("CHECK_IN_DATE", "N/A")
                check_out_date = reservation.get("CHECK_OUT_DATE", "N/A")

                # Prepare values for table
                values = (
                    invoice_id,  # Invoice ID
                    f"R{reservation_id}",  # Reservation ID
                    guest_name,  # Guest Name
                    room_number,  # Room Number
                    check_in_date,  # Check In
                    check_out_date,  # Check Out
                    f"₱{total_amount:.2f}",  # Amount
                    payment_status  # Payment Status
                )

                # Determine row color based on payment status
                if payment_status in ["Paid", "Completed"]:
                    tag = 'paid'
                elif payment_status == "Pending":
                    tag = 'pending'
                elif payment_status == "Overdue":
                    tag = 'overdue'
                else:
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'

                item_id = self.treeview.insert("", "end", values=values, tags=(tag,))

                # Store the reservation ID for later retrieval
                self.treeview.item(item_id, tags=(tag, f"res_{reservation_id}"))

        except Exception as e:
            log(f"Error populating billing records: {str(e)}", "ERROR")
            self.treeview.insert("", "end", values=("Error loading billing data", "", "", "", "", "", "", ""))

    def filter_table(self):
        search_text = self.search_var.get().lower().strip()
        selected_status = self.filter_var.get()

        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        try:
            # Get all reservations
            reservations = self.reservation_model.get_all_reservations()
            if not reservations:
                self.treeview.insert("", "end", values=("-", "-", "-", "-", "-", "-", "-", "-"))
                return

            # Process and filter reservations using billing model (same as populate_billing_records)
            filtered_count = 0
            for i, reservation in enumerate(reservations):
                reservation_id = reservation.get("RESERVATION_ID")
                guest_id = reservation.get("GUEST_ID")
                room_id = reservation.get("ROOM_ID")

                guest_name = "Unknown Guest"
                room_number = "N/A"

                # Get guest details
                try:
                    guest = self.guest_model.get_guest_by_id(guest_id)
                    if guest:
                        guest_name = f"{guest.get('FIRST_NAME', 'Guest')} {guest.get('LAST_NAME', '')}"
                except:
                    pass

                # Get room details
                try:
                    room_data = self.room_model.get_room_data_with_type(room_id)
                    if room_data:
                        room_number = room_data.get('ROOM_NUMBER', 'N/A')
                except:
                    pass

                # Get billing summary from billing model (consistent with populate_billing_records)
                billing_summary = self.billing_model.get_billing_summary_by_reservation(reservation_id)

                if billing_summary:
                    invoice_id = billing_summary['invoice_id']
                    total_amount = billing_summary['total_amount']
                    payment_status = billing_summary['payment_status']
                else:
                    continue  # Skip this reservation if we can't get billing info

                # Format dates for display
                check_in_date = reservation.get("CHECK_IN_DATE", "N/A")
                check_out_date = reservation.get("CHECK_OUT_DATE", "N/A")

                # Apply filters
                if selected_status != "All Status" and payment_status != selected_status:
                    continue

                if search_text and search_text not in guest_name.lower() and search_text not in invoice_id.lower():
                    continue

                # Add to treeview
                values = (
                    invoice_id, f"R{reservation_id}", guest_name, room_number,
                    check_in_date, check_out_date, f"₱{total_amount:.2f}", payment_status
                )

                if payment_status == "Paid":
                    tag = 'paid'
                elif payment_status == "Pending":
                    tag = 'pending'
                elif payment_status == "Overdue":
                    tag = 'overdue'
                else:
                    tag = 'evenrow' if filtered_count % 2 == 0 else 'oddrow'

                item_id = self.treeview.insert("", "end", values=values, tags=(tag,))
                self.treeview.item(item_id, tags=(tag, f"res_{reservation_id}"))
                filtered_count += 1

            if filtered_count == 0:
                self.treeview.insert("", "end", values=("No matching records", "", "", "", "", "", "", ""))

        except Exception as e:
            log(f"Error filtering billing records: {str(e)}", "ERROR")

    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            billing_values = self.treeview.item(selected_item[0], "values")
            if billing_values and billing_values[0] != "-":
                self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.40, relheight=1)
                self.show_billing_info(billing_values)
        else:
            self.right_frame.place_forget()

    def show_billing_info(self, billing_values):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Set up header with navigation and controls
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                    border_width=0, border_color=self.BORDER_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(3, 0))
        header_frame.grid_columnconfigure(0, weight=1)

        # Right Header Frame with buttons
        right_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        right_header_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="e")

        # Get reservation ID from billing values
        reservation_id_str = billing_values[1]  # "R123" format
        reservation_id = int(reservation_id_str[1:]) if reservation_id_str.startswith("R") else None

        # Action buttons
        view_invoice_button = ctk.CTkButton(right_header_frame, text="View Invoice", text_color="white", width=80, height=30,
                                           corner_radius=4, fg_color="#2563eb",
                                           command=lambda: self.view_invoice(billing_values))
        view_invoice_button.grid(column=0, row=0, padx=(0, 5))

        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                   corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                   command=lambda: [self.right_frame.place_forget(),
                                                   self.treeview.selection_remove(self.treeview.selection())],
                                   font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=2, row=0, padx=(5, 10))

        # Content area
        scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))
        scrollable.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Billing Details", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        # Billing Information
        info_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        info_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Build billing info dictionary
        billing_info = {
            "Invoice ID": billing_values[0],
            "Reservation ID": billing_values[1],
            "Guest Name": billing_values[2],
            "Room Number": billing_values[3],
            "Check-in Date": billing_values[4],
            "Check-out Date": billing_values[5],
            "Total Amount": billing_values[6],
            "Payment Status": billing_values[7],
            "Payment Method": "N/A",
            "Transaction Date": "N/A"
        }

        # Add info rows
        info_rows = [(key, value) for key, value in billing_info.items()]

        info_frame.grid_columnconfigure(0, minsize=120, weight=1, uniform="info")
        info_frame.grid_columnconfigure(1, minsize=180, weight=1, uniform="info")

        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew")

            # Value "cell" frame
            value_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            value_cell.grid(row=index, column=1, sticky="nsew")

            # Label text
            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 12), anchor="w",
                                      wraplength=110, justify="left")
            label_text.pack(fill="both", expand=True, padx=8, pady=8)

            # Value text
            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 12),
                                      anchor="w", wraplength=170, justify="left")
            value_text.pack(fill="both", expand=True, padx=8, pady=8)

    def process_payment_popup(self, billing_data=None):
        """Open payment processing dialog"""
        if not billing_data:
            selected_item = self.treeview.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a billing record to process payment.")
                return
            billing_data = self.treeview.item(selected_item[0], "values")

        if billing_data[7] in ["Paid", "Completed"]:
            messagebox.showinfo("Payment Complete", "This invoice has already been paid.")
            return

        # Get reservation ID
        reservation_id_str = billing_data[1]
        reservation_id = int(reservation_id_str[1:]) if reservation_id_str.startswith("R") else None

        if not reservation_id:
            messagebox.showerror("Error", "Could not determine reservation ID.")
            return

        # Create payment dialog
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("Process Payment")
        payment_window.geometry("450x650")
        payment_window.grab_set()
        payment_window.configure(fg_color=self.BG_COLOR_2)

        # Payment form
        ctk.CTkLabel(payment_window, text="Process Payment",
                    font=("Roboto Condensed", 20, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(payment_window, text=f"Invoice: {billing_data[0]}",
                    font=("Roboto Condensed", 14)).pack(pady=5)
        ctk.CTkLabel(payment_window, text=f"Guest: {billing_data[2]}",
                    font=("Roboto Condensed", 14)).pack(pady=5)
        ctk.CTkLabel(payment_window, text=f"Amount: {billing_data[6]}",
                    font=("Roboto Condensed", 16, "bold")).pack(pady=10)

        # Payment method
        ctk.CTkLabel(payment_window, text="Payment Method:",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        payment_method_var = ctk.StringVar(value="Cash")
        payment_method_dropdown = ctk.CTkComboBox(
            payment_window,
            values=["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Check"],
            variable=payment_method_var,
            width=200
        )
        payment_method_dropdown.pack(pady=5)

        # Amount paid
        ctk.CTkLabel(payment_window, text="Amount Paid:",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        amount_entry = ctk.CTkEntry(payment_window, width=200)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, billing_data[6].replace("₱", "").replace(",", ""))

        # Transaction ID
        ctk.CTkLabel(payment_window, text="Transaction ID (Optional):",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        transaction_entry = ctk.CTkEntry(payment_window, width=200)
        transaction_entry.pack(pady=5)

        # Notes
        ctk.CTkLabel(payment_window, text="Notes (Optional):",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        notes_entry = ctk.CTkTextbox(payment_window, width=300, height=60)
        notes_entry.pack(pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(payment_window, fg_color="transparent")
        button_frame.pack(pady=20)

        def confirm_payment():
            try:
                amount_paid = float(amount_entry.get())

                # First generate invoice if it doesn't exist
                invoice_id = self.billing_model.generate_invoice(reservation_id)

                if not invoice_id:
                    messagebox.showerror("Error", "Could not generate invoice.")
                    return

                # Prepare payment data
                payment_data = {
                    'AMOUNT_PAID': amount_paid,
                    'PAYMENT_METHOD': payment_method_var.get(),
                    'TRANSACTION_ID': transaction_entry.get() or None,
                    'NOTES': notes_entry.get("1.0", "end-1c") or None,
                    'PAYMENT_DATE': datetime.now().date()
                }

                # Process payment using billing model
                success = self.billing_model.process_payment(invoice_id, payment_data)

                if success:
                    messagebox.showinfo("Payment Processed", "Payment has been processed successfully!")
                    payment_window.destroy()
                    self.populate_billing_records()  # Refresh the table
                    self.right_frame.place_forget()
                else:
                    messagebox.showerror("Error", "Failed to process payment.")

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
            except Exception as e:
                log(f"Error processing payment: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        ctk.CTkButton(button_frame, text="Process Payment",
                     fg_color="#28a745", hover_color="#218838",
                     command=confirm_payment).pack(side="left", padx=10)

        ctk.CTkButton(button_frame, text="Cancel",
                     fg_color="#dc3545", hover_color="#c82333",
                     command=payment_window.destroy).pack(side="left", padx=10)

    def view_invoice(self, billing_data):
        """Open the invoice page for the selected billing record"""
        from ui.billing.billingInvoicePage import BillingInvoicePage

        invoice_window = ctk.CTkToplevel(self)
        invoice_window.title(f"Invoice - {billing_data[0]}")

        # Create invoice page
        invoice_page = BillingInvoicePage(master=invoice_window, invoice_data=billing_data)

    def refresh_data(self):
        """Refresh the billing table"""
        self.populate_billing_records()

    def process_refund_popup(self, billing_data=None):
        """Open refund processing dialog"""
        if not billing_data:
            selected_item = self.treeview.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a billing record to process refund.")
                return
            billing_data = self.treeview.item(selected_item[0], "values")

        if billing_data[7] not in ["Paid", "Completed"]:
            messagebox.showinfo("Refund Not Applicable", "This invoice is not eligible for a refund.")
            return

        # Get reservation ID
        reservation_id_str = billing_data[1]
        reservation_id = int(reservation_id_str[1:]) if reservation_id_str.startswith("R") else None

        if not reservation_id:
            messagebox.showerror("Error", "Could not determine reservation ID.")
            return

        # Create refund dialog
        refund_window = ctk.CTkToplevel(self)
        refund_window.title("Process Refund")
        refund_window.geometry("450x650")
        refund_window.grab_set()
        refund_window.configure(fg_color=self.BG_COLOR_2)

        # Refund form
        ctk.CTkLabel(refund_window, text="Process Refund",
                    font=("Roboto Condensed", 20, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(refund_window, text=f"Invoice: {billing_data[0]}",
                    font=("Roboto Condensed", 14)).pack(pady=5)
        ctk.CTkLabel(refund_window, text=f"Guest: {billing_data[2]}",
                    font=("Roboto Condensed", 14)).pack(pady=5)
        ctk.CTkLabel(refund_window, text=f"Amount: {billing_data[6]}",
                    font=("Roboto Condensed", 16, "bold")).pack(pady=10)

        # Refund method
        ctk.CTkLabel(refund_window, text="Refund Method:",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        refund_method_var = ctk.StringVar(value="Cash")
        refund_method_dropdown = ctk.CTkComboBox(
            refund_window,
            values=["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Check"],
            variable=refund_method_var,
            width=200
        )
        refund_method_dropdown.pack(pady=5)

        # Amount refunded
        ctk.CTkLabel(refund_window, text="Amount Refunded:",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        amount_refund_entry = ctk.CTkEntry(refund_window, width=200)
        amount_refund_entry.pack(pady=5)
        amount_refund_entry.insert(0, billing_data[6].replace("₱", "").replace(",", ""))

        # Transaction ID
        ctk.CTkLabel(refund_window, text="Transaction ID (Optional):",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        transaction_refund_entry = ctk.CTkEntry(refund_window, width=200)
        transaction_refund_entry.pack(pady=5)

        # Notes
        ctk.CTkLabel(refund_window, text="Notes (Optional):",
                    font=("Roboto Condensed", 14)).pack(pady=(10, 5))

        notes_refund_entry = ctk.CTkTextbox(refund_window, width=300, height=60)
        notes_refund_entry.pack(pady=5)

        # Buttons
        refund_button_frame = ctk.CTkFrame(refund_window, fg_color="transparent")
        refund_button_frame.pack(pady=20)

        def confirm_refund():
            try:
                amount_refunded = float(amount_refund_entry.get())

                # Prepare refund data
                refund_data = {
                    'AMOUNT_REFUNDED': amount_refunded,
                    'REFUND_METHOD': refund_method_var.get(),
                    'TRANSACTION_ID': transaction_refund_entry.get() or None,
                    'NOTES': notes_refund_entry.get("1.0", "end-1c") or None,
                    'REFUND_DATE': datetime.now().date()
                }

                # Process refund using billing model
                success = self.billing_model.process_refund(reservation_id, refund_data)

                if success:
                    messagebox.showinfo("Refund Processed", "Refund has been processed successfully!")
                    refund_window.destroy()
                    self.populate_billing_records()  # Refresh the table
                    self.right_frame.place_forget()
                else:
                    messagebox.showerror("Error", "Failed to process refund.")

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
            except Exception as e:
                log(f"Error processing refund: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        ctk.CTkButton(refund_button_frame, text="Process Refund",
                     fg_color="#dc3545", hover_color="#c82333",
                     command=confirm_refund).pack(side="left", padx=10)

        ctk.CTkButton(refund_button_frame, text="Cancel",
                     fg_color="#28a745", hover_color="#218838",
                     command=refund_window.destroy).pack(side="left", padx=10)
