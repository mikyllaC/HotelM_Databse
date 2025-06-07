import customtkinter as ctk
from tkinter import ttk, messagebox


class BillingPaymentPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#F5F5F5")
        self.create_widgets()


# ============== Widget Creation ==============
    def create_widgets(self):


        # ========== Title ==========
        label = ctk.CTkLabel(self,
                             text="Billing & Payment",
                             font=("Arial", 24, "bold"),
                             text_color="black")
        label.pack(pady=(40, 30))


        # ========== Buttons ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        button_frame.pack(pady=(10, 0), padx=(20, 10), fill="x")
        button_frame.pack_propagate(False)

        button_kwargs = dict(font=("Arial", 15, "bold"), width=200, height=40, text_color="white",
                             fg_color="#2563eb", hover_color="#1d4ed8")

        view_invoice_info_btn = ctk.CTkButton(button_frame,
                                              text="View Invoice Information",
                                              command=self.show_invoice_frame,
                                              **button_kwargs)
        view_invoice_info_btn.pack(side="right", padx=(20, 10), pady=10)

        update_btn = ctk.CTkButton(button_frame,
                                   text="Update Billing",
                                   command=self.update_billing,
                                   **button_kwargs)
        update_btn.pack(side="right", padx=(20, 10), pady=10)


        # ========== Billing Table ==========
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(pady=(10, 10), padx=(0, 10), fill="both", expand=True)

        columns = ("Invoice No.", "Guest Name", "Room Type", "Nights", "Amount", "Status")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), foreground="#374151")
        style.configure("Treeview", font=("Courier", 11), rowheight=25)
        style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", "#1a1a1a")])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=150)

        self.tree.tag_configure("even_row", background="#f7f7f7")
        self.tree.tag_configure("odd_row", background="#ffffff")

        self.tree.pack(fill="both", expand=True, padx=(20, 10), pady=(0, 10))

        # Treeview selection binding
        # self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Populate billing history
        self.populate_billing_history()


    def populate_billing_history(self):
        # Sample billing data
        billing_data = [
            # invoice_no, guest_name, room_type, nights, amount, status
            ("INV1000", "Guest 1", "Deluxe", 3, 4500, "Paid"),
            ("INV1001", "Guest 2", "Deluxe", 2, 3200, "Pending"),
            ("INV1002", "Guest 3", "Deluxe", 5, 7800, "Paid"),
            ("INV1003", "Guest 4", "Deluxe", 1, 2500, "Pending"),
            ("INV1004", "Guest 5", "Deluxe", 4, 6000, "Paid")
        ]

        # clears treeview of old data before inserting the new records.
        for item in self.tree.get_children():
            self.tree.delete(item)

        for data in billing_data:
            invoice_no, guest_name, room_type, nights, amount, status = data
            self.tree.insert("", "end",
                             values=(invoice_no, guest_name, room_type, nights, f"${amount:.2f}", status))


    # def on_tree_select(self):
    #     selected = self.tree.focus()
    #     if selected:
    #         data = self.tree.item(selected, "values")


    def show_invoice_frame(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning("No Selection", "Please select an invoice to view.")
            return

        data = self.tree.item(selected, "values")

        if data:
            # Open BillingInvoicePage in a new window and pass the selected invoice data
            from ui.billing.billingInvoicePage import BillingInvoicePage

            invoice_window = ctk.CTkToplevel(self)
            invoice_window.title(f"Invoice {data[0]}")
            BillingInvoicePage(master=invoice_window, invoice_data=data)


    def update_billing(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning("No Selection", "Please select a billing record to update.")
            return

        data = self.tree.item(selected, "values")
        invoice_no, guest_name, room_type, nights, amount, status = data

        popup = ctk.CTkToplevel(self)
        popup.title(f"Update Billing - {invoice_no}")
        popup.geometry("400x300")
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"Invoice No: {invoice_no}", font=("Arial", 14, "bold")).pack(pady=(20, 5))

        status_label = ctk.CTkLabel(popup, text="Status:")
        status_label.pack(pady=5)
        status_var = ctk.StringVar(value=status)
        status_dropdown = ctk.CTkComboBox(popup, values=["Paid", "Pending"], variable=status_var)
        status_dropdown.pack()

        def save_update():
            new_status = status_var.get()
            self.tree.item(selected, values=(invoice_no, guest_name, room_type, nights, amount, new_status))
            popup.destroy()

        save_btn = ctk.CTkButton(popup, text="Save Changes", command=save_update)
        save_btn.pack(pady=20)


# ========== Preview Frame as App ==========
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1400x900")
    root.title("Billing and Payments Test")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    page = BillingPaymentPage(root)
    page.pack(fill="both", expand=True)

    root.mainloop()
