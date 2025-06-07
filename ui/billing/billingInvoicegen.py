import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

#Notes ni Sofia
#Sa may billing na GUI, may button na "View Invoice" eto dapat lalabas.
#Up to lead dev yung pag lagay ng data here from database.
#Invoice neto if possible, maging printable siya by saving it as PDF.

class BillingInvoicePage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.master.geometry("1600x800")

    def create_widgets(self):
        # Main Invoice Frame
        self.invoice_frame = ctk.CTkFrame(self, fg_color="#F5F5F5")
        self.invoice_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sample Invoice Breakdown Label
        sample_breakdown_label = ctk.CTkLabel(
            self.invoice_frame,
            text="Invoice Breakdown",
            font=("Arial", 20, "bold"),
            anchor="w",
            justify="left"
        )
        sample_breakdown_label.pack(anchor="w", padx=20, pady=(20, 20))

        # Invoice Number Frame
        invoice_number_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        invoice_number_frame.pack(fill="x", padx=10, pady=(0, 20))

        invoice_number_label = ctk.CTkLabel(
            invoice_number_frame,
            text="Invoice Number:",
            font=("Arial", 15),
            anchor="w"
        )
        invoice_number_label.pack(anchor="w", padx=10, pady=2)

        # Create a container for Guest and Booking Info labels
        labels_row = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        labels_row.pack(fill="x", padx=10, pady=(0, 0))

        # Guest Information Label (left)
        guest_info_category_label = ctk.CTkLabel(
            labels_row,
            text="Guest Information",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        guest_info_category_label.pack(side="left", fill="x", expand=True, padx=(10, 50))

        # Booking Information Label (right)
        booking_info_category_label = ctk.CTkLabel(
            labels_row,
            text="Booking Information",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        booking_info_category_label.pack(side="left", fill="x", expand=True)

        # Guest and Booking Information Side-by-Side
        info_container = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=10, pady=(0, 20))

        # Guest Info (left)
        guest_info_left = ctk.CTkFrame(info_container, fg_color="transparent")
        guest_info_left.pack(side="left", fill="both", expand=True)

        guest_name_label = ctk.CTkLabel(
            guest_info_left,
            text="Guest Name:",
            font=("Arial", 16),
            anchor="w"
        )
        guest_name_label.pack(anchor="w", padx=20, pady=2)

        guest_id_label = ctk.CTkLabel(
            guest_info_left,
            text="Guest ID:",
            font=("Arial", 16),
            anchor="w"
        )
        guest_id_label.pack(anchor="w", padx=20, pady=2)

        guest_email_label = ctk.CTkLabel(
            guest_info_left,
            text="Email:",
            font=("Arial", 16),
            anchor="w"
        )
        guest_email_label.pack(anchor="w", padx=20, pady=2)

        guest_contact_label = ctk.CTkLabel(
            guest_info_left,
            text="Contact Number:",
            font=("Arial", 16),
            anchor="w"
        )
        guest_contact_label.pack(anchor="w", padx=20, pady=2)

        # Booking Info (right)
        booking_info_right = ctk.CTkFrame(info_container, fg_color="transparent")
        booking_info_right.pack(side="left", fill="both", expand=True, padx=(40, 0))

        room_number_label = ctk.CTkLabel(
            booking_info_right,
            text="Room Number:",
            font=("Arial", 16),
            anchor="w"
        )
        room_number_label.pack(anchor="w", padx=10, pady=2)

        checkin_label = ctk.CTkLabel(
            booking_info_right,
            text="Check-in Date:",
            font=("Arial", 16),
            anchor="w"
        )
        checkin_label.pack(anchor="w", padx=10, pady=2)

        checkout_label = ctk.CTkLabel(
            booking_info_right,
            text="Check-out Date:",
            font=("Arial", 16),
            anchor="w"
        )
        checkout_label.pack(anchor="w", padx=10, pady=2)

        # Payment Breakdown
        payment_columns = ("Service Description", "Subtotal", "Tax", "Total")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 14))

        self.payment_tree = ttk.Treeview(self.invoice_frame, 
                         columns=payment_columns, 
                         show="headings", height=5
                         )
        for col in payment_columns:
            self.payment_tree.heading(col, text=col)
            self.payment_tree.column(col, width=400)
        self.payment_tree.pack(padx=20, pady=20)

        # Billing Summary Frame
        billing_summary_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        billing_summary_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Subtotal
        subtotal_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Subtotal:",
            font=("Arial", 16),
            anchor="e",
            width=200
        )
        subtotal_label.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=2)
        subtotal_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 16),
            anchor="w"
        )
        subtotal_value.grid(row=0, column=1, sticky="w", padx=(0, 30), pady=2)

        # Tax
        tax_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Tax:",
            font=("Arial", 16),
            anchor="e",
            width=200
        )
        tax_label.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=2)
        tax_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 16),
            anchor="w"
        )
        tax_value.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=2)

        # Grand Total
        total_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Grand Total:",
            font=("Arial", 18, "bold"),
            anchor="e",
            width=200
        )
        total_label.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=2)
        total_value = ctk.CTkLabel(
            billing_summary_frame,
            text="₱0.00",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        total_value.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=2)

        # Payment Status
        payment_status_label = ctk.CTkLabel(
            billing_summary_frame,
            text="Payment Status:",
            font=("Arial", 16),
            anchor="e",
            width=200
        )
        payment_status_label.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=2)
        payment_status_value = ctk.CTkLabel(
            billing_summary_frame,
            text="Unpaid",
            font=("Arial", 16),
            anchor="w",
            text_color="#D32F2F"
        )
        payment_status_value.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=2)

        # Notes
        notes_label = ctk.CTkLabel(
            self.invoice_frame,
            text="Notes: Thank you for staying with us! Please settle your bill at the front desk.",
            font=("Arial", 14, "italic"),
            anchor="w",
            text_color="#616161"
        )
        notes_label.pack(anchor="w", padx=20, pady=(0, 10))

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

         # Download Invoice Button
        download_button = ctk.CTkButton(
            buttons_frame,
            text="Download Invoice",
            width=170,
            height=40,
            font=("Arial", 14, "bold"),
            text_color="white",
            fg_color="#4CAF50",  # Green color
        )
        download_button.pack(side="right")

       #CAncel button
        print_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=150,
            height=40,
            fg_color="#B0B0B0",
            font=("Arial", 14, "bold")
            , text_color="white"
        )
        print_button.pack(side="right", padx=(20, 10))


        def download_invoice():
            messagebox.showinfo("Download Invoice", "Invoice has been downloaded successfully.")

        download_button.configure(command=download_invoice)
        

# For standalone testing
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Billing Invoice Page")
    BillingInvoicePage(master=root)
    root.mainloop()