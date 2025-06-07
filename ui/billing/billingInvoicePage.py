from tkinter import ttk, messagebox
import customtkinter as ctk

# Notes ni Sofia
# Sa may billing na GUI, may button na "View Invoice" eto dapat lalabas.
# Up to lead dev yung pag lagay ng data here from database.
# Invoice neto if possible, maging printable siya by saving it as PDF.

class BillingInvoicePage(ctk.CTkFrame):
    def __init__(self, master=None, invoice_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)
        self.invoice_data = invoice_data
        self.master.geometry("1200x850")

        self.create_widgets()

        if self.invoice_data:
            self.populate_invoice_fields(self.invoice_data)


    def create_widgets(self):
        # Main Invoice Frame
        self.invoice_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12)
        self.invoice_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            self.invoice_frame,
            text="Invoice Details",
            font=("Arial", 22, "bold"),
            text_color="#222"
        )
        title_label.pack(anchor="center", pady=(10, 25))

        # Invoice Number Frame
        invoice_number_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        invoice_number_frame.pack(fill="x", padx=30, pady=(0, 18))
        self.invoice_number_label = ctk.CTkLabel(
            invoice_number_frame,
            text="Invoice Number:",
            font=("Arial", 15, "bold"),
            text_color="#444",
            anchor="w"
        )
        self.invoice_number_label.pack(anchor="w", padx=10, pady=2)

        # Guest and Booking Info Row
        info_row = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        info_row.pack(fill="x", padx=20, pady=(0, 10))  # Increased padx

        # Guest Info
        guest_info = ctk.CTkFrame(info_row, fg_color="#f7f7f7", corner_radius=8)
        guest_info.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=5)
        ctk.CTkLabel(guest_info,
                     text="Guest Information",
                     font=("Arial", 16, "bold"),
                     text_color="#222").pack(anchor="w", padx=20, pady=(10, 5))
        self.guest_name_label = ctk.CTkLabel(guest_info,
                                             text="Guest Name:",
                                             font=("Arial", 14),
                                             text_color="#222")
        self.guest_name_label.pack(anchor="w", padx=20, pady=2)
        self.guest_id_label = ctk.CTkLabel(guest_info,
                                           text="Guest ID:",
                                           font=("Arial", 14),
                                           text_color="#222")
        self.guest_id_label.pack(anchor="w", padx=20, pady=2)
        self.guest_email_label = ctk.CTkLabel(guest_info,
                                              text="Email:",
                                              font=("Arial", 14),
                                              text_color="#222")
        self.guest_email_label.pack(anchor="w", padx=20, pady=2)
        self.guest_contact_label = ctk.CTkLabel(guest_info,
                                                text="Contact Number:",
                                                font=("Arial", 14),
                                                text_color="#222")
        self.guest_contact_label.pack(anchor="w", padx=20, pady=2)

        # Booking Info
        booking_info = ctk.CTkFrame(info_row, fg_color="#f7f7f7", corner_radius=8)
        booking_info.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=5)
        ctk.CTkLabel(booking_info,
                     text="Booking Information",
                     font=("Arial", 16, "bold"),
                     text_color="#222").pack(anchor="w", padx=20, pady=(10, 5))
        self.room_number_label = ctk.CTkLabel(booking_info,
                                              text="Room Number:",
                                              font=("Arial", 14),
                                              text_color="#222")
        self.room_number_label.pack(anchor="w", padx=20, pady=2)
        self.checkin_label = ctk.CTkLabel(booking_info,
                                          text="Check-in Date:",
                                          font=("Arial", 14),
                                          text_color="#222")
        self.checkin_label.pack(anchor="w", padx=20, pady=2)
        self.checkout_label = ctk.CTkLabel(booking_info,
                                           text="Check-out Date:",
                                           font=("Arial", 14),
                                           text_color="#222")
        self.checkout_label.pack(anchor="w", padx=20, pady=2)

        # Divider
        divider = ctk.CTkFrame(self.invoice_frame, fg_color="#e5e7eb", height=2)
        divider.pack(fill="x", padx=20, pady=(10, 10))  # Increased padx

        # Payment Breakdown Table
        payment_columns = ("Service Description", "Subtotal", "Tax", "Total")
        style = ttk.Style()
        style.configure("Invoice.Treeview.Heading", font=("Arial", 13, "bold"), foreground="#444")
        style.configure("Invoice.Treeview", font=("Courier", 12), rowheight=26)
        self.payment_tree = ttk.Treeview(self.invoice_frame,
                                         columns=payment_columns,
                                         show="headings", height=7,
                                         style="Invoice.Treeview"
                                         )
        for col in payment_columns:
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, width=200, anchor="w")  # Increased width
        self.payment_tree.pack(padx=20, pady=10, fill="x")  # Increased padx
        # Alternate row colors
        self.payment_tree.tag_configure('oddrow', background='#fafafa')
        self.payment_tree.tag_configure('evenrow', background='#f0f0f0')

        # Billing Summary Frame
        billing_summary_frame = ctk.CTkFrame(self.invoice_frame, fg_color="#f7f7f7", corner_radius=8)
        billing_summary_frame.pack(fill="x", padx=20, pady=(0, 20))  # Increased padx
        # Subtotal
        subtotal_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Subtotal:",
            font=("Arial", 15),
            anchor="e",
            width=200,
            text_color="#222"
        )
        subtotal_label.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=2)
        subtotal_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 15),
            anchor="w",
            text_color="#222"
        )
        subtotal_value.grid(row=0, column=1, sticky="w", padx=(0, 30), pady=2)
        # Tax
        tax_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Tax:",
            font=("Arial", 15),
            anchor="e",
            width=200,
            text_color="#222"
        )
        tax_label.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=2)
        tax_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 15),
            anchor="w",
            text_color="#222"
        )
        tax_value.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=2)
        # Grand Total
        total_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Grand Total:",
            font=("Arial", 16, "bold"),
            anchor="e",
            width=200,
            text_color="#111"
        )
        total_label.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=2)
        total_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 16, "bold"),
            anchor="w",
            text_color="#111"
        )
        total_value.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=2)
        # Payment Status
        payment_status_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Payment Status:",
            font=("Arial", 15),
            anchor="e",
            width=200,
            text_color="#222"
        )
        payment_status_label.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=2)
        payment_status_value = ctk.CTkLabel(
            billing_summary_frame,
            text="Unpaid",
            font=("Arial", 15),
            anchor="w",
            text_color="#D32F2F"
        )
        payment_status_value.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=2)

        # Notes
        notes_label = ctk.CTkLabel(
            self.invoice_frame,
            text="Note: Thank you for staying with us! Please settle your bill at the front desk.",
            font=("Arial", 13, "italic"),
            anchor="w",
            text_color="#616161"
        )
        notes_label.pack(anchor="w", padx=20, pady=(0, 10))  # Increased padx

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))  # Increased padx
        download_button = ctk.CTkButton(
            buttons_frame,
            text="Download Invoice",
            width=170,
            height=40,
            font=("Arial", 14, "bold"),
            text_color="white",
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        download_button.pack(side="right")
        print_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=150,
            height=40,
            fg_color="#B0B0B0",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        print_button.pack(side="right", padx=(20, 10))
        # Pop up message if download button is clicked
        def download_invoice():
            messagebox.showinfo("Download Invoice", "Invoice has been downloaded successfully.")

        download_button.configure(command=download_invoice)


    def populate_invoice_fields(self, data):
        # data: (invoice_no, guest_name, room_type, nights, amount, status)
        invoice_no, guest_name, room_type, nights, amount, status = data
        self.invoice_number_label.configure(text=f"Invoice Number: {invoice_no}")
        self.guest_name_label.configure(text=f"Guest Name: {guest_name}")
        self.guest_id_label.configure(text=f"Guest ID: -")
        self.guest_email_label.configure(text=f"Email: -")
        self.guest_contact_label.configure(text=f"Contact Number: -")
        self.room_number_label.configure(text=f"Room Number: {room_type}")
        self.checkin_label.configure(text=f"Check-in Date: -")
        self.checkout_label.configure(text=f"Check-out Date: -")
        # Optionally, fill payment_tree and summary if you have more data


# For standalone testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Billing Invoice Page")
    root.geometry("1400x900")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    BillingInvoicePage(master=root)
    root.mainloop()
