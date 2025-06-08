import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

#Notes ni Sofia sa GUI 
#1. Added create guest beside create reservation
#2. Fixed geometry of window to 1600x800
#3. added Guest ID in table 
#4. Removed Rooms in category

ctk.set_appearance_mode("light")

class GuestListPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#f0f0f0")
        self.master.geometry("1600x800")


        # Placeholder Data
        self.guest_data = [
            ["Guest Name", "Guest ID" ,"Contact Information", "Status"],
            ["Sunday", "000-00", "0916-123-1234", "Checked In"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
        ]

        self.build_ui()

    def build_ui(self):
        self.build_title_label()
        self.build_right_frame()
        self.build_search_filter_bar()
        self.build_left_table()

    def build_title_label(self):
        title_label = ctk.CTkLabel(self, text="Guest Management", font=("Arial", 28, "bold"))
        title_label.pack(side="top", anchor="n", pady=(35, 45), padx=(10, 0))

    def build_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, width=300, height=738, corner_radius=10, border_width=1)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack_forget()

        right_label = ctk.CTkLabel(self.right_frame, text="Guest Information", font=("Arial", 18, "bold"))
        right_label.pack(pady=10)

        close_button = ctk.CTkButton(
            self.right_frame,
            text="X",
            command=self.close_right_frame,
            width=20,
            height=20,
            corner_radius=10
            , fg_color="#e57373", hover_color="#c62828"
        )
        close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

        self.update_payment_button = ctk.CTkButton(
            self.right_frame,
            text="Update Payment",
            font=("Arial", 16, "bold"),
            width=180,
            height=40,
            command=self.update_payment_popup
        )
        self.update_payment_button.pack(side="bottom", padx=20, pady=10)

        self.edit_guest_button = ctk.CTkButton(
            self.right_frame,
            text="Edit Guest Info",
            font=("Arial", 16, "bold"),
            width=180,
            height=40
        )
        self.edit_guest_button.pack(side="bottom", padx=20, pady=(0, 10))

    #Close right frame function
    def close_right_frame(self):
        self.right_frame.pack_forget()

    def show_guest_info(self, guest_info):
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Guest Information":
                continue
            if isinstance(widget, ctk.CTkButton):
                continue
            widget.destroy()
        # Display guest information (placeholder data)
        labels = self.guest_data[0]
        extra_info = {
            "Email": "sunday@example.com",
            "Address": "123 Main St, City",
            "Check-in Date": "2023-10-01",
            "Check-out Date": "2023-10-05",
        }

        wraplength = 200

        for i, value in enumerate(guest_info):
            info_label = ctk.CTkLabel(self.right_frame, text=f"{labels[i]}: {value}", font=("Arial", 14),
                                      wraplength=wraplength, justify="left")
            info_label.pack(anchor="w", padx=20, pady=2, fill="x")

        for key, value in extra_info.items():
            extra_label = ctk.CTkLabel(self.right_frame, text=f"{key}: {value}", font=("Arial", 14),
                                       wraplength=wraplength, justify="left")
            extra_label.pack(anchor="w", padx=20, pady=2, fill="x")

    def build_search_filter_bar(self):
        self.search_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_filter_frame.pack(side="top", anchor="w", padx=(35, 0), expand=True, fill="x")

        # Create Reservation Button
        create_reservation_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Create Reservation",
            font=("Arial", 16, "bold"),
            width=180,
            height=36
        )
        create_reservation_button.pack(side="left", padx=(0, 10))

        # Create Guest Button
        create_guest_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Create Guest",
            font=("Arial", 16, "bold"),
            width=150,
            height=36,
            command=self.create_guest_popup
        )
        create_guest_button.pack(side="left", padx=(0, 10))
        
        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.search_filter_frame,
            width=220,
            height=36,
            placeholder_text="Search guest name...",
            textvariable=self.search_var,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = tk.StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.search_filter_frame,
            width=160,
            height=36,
            values=["All Status", "Checked In", "Checked Out", "Reserved"],
            variable=self.filter_var,
            font=("Arial", 14)
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        # Search/Filter Event Binding
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.filter_table())

        # Quote Text
        quote_label = ctk.CTkLabel(
            self.search_filter_frame,
            text="'Let the pain teach you how to dougie'",
            font=("Arial", 12, "italic", "bold"),
            text_color="#888888"
        )
        quote_label.pack(side="right", padx=75)

    def filter_table(self):
        search_text = self.search_var.get().lower()
        selected_status = self.filter_var.get()

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for row in self.guest_data[1:]:
            name, _, _, status = row
            if (search_text in name.lower() or not search_text) and \
               (selected_status == "All Status" or status == selected_status):
                self.treeview.insert("", "end", values=row)

    #Function to update payment status window pop up
    def update_payment_popup(self):
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("Update Payment")
        payment_window.geometry("400x300")

        ctk.CTkLabel(payment_window, text="Update Payment", font=("Arial", 20, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(payment_window, text="Enter new payment status:", font=("Arial", 14)).pack(pady=(30, 10))

        payment_status_var = tk.StringVar(value="Paid")
        payment_status_combobox = ctk.CTkComboBox(
            payment_window,
            values=["Paid", "Unpaid", "Pending", "Refunded"],
            variable=payment_status_var,
            width=200
        )
        payment_status_combobox.pack(pady=10)

        def save_payment():
            payment_window.destroy()

        ctk.CTkButton(payment_window, text="Update", command=save_payment, width=120).pack(pady=20)

    #Function for guest information window pop up
    def build_left_table(self):
        self.left_frame = ctk.CTkFrame(self, width=1250, height=738, corner_radius=10,
                                       border_width=0, fg_color="transparent")
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side="left", padx=(10, 1), pady=(15, 10), fill="y", anchor="n")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 15, "bold"), anchor="w")
        style.configure("Treeview", rowheight=30, font=("Courier", 14), anchor="w")

        self.treeview = ttk.Treeview(self.left_frame, columns=self.guest_data[0], show="headings", height=20)
        self.treeview.pack(expand=True, fill="both", padx=10, pady=20)

        for col in self.guest_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, width=200, anchor="w")

        for row in self.guest_data[1:]:
            self.treeview.insert("", "end", values=row)

        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

    #Function to handle row selection in the table
    def on_row_select(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item[0], "values")
            if item_values and item_values[0] != "-":
                self.right_frame.pack(side="left", padx=(1, 20), pady=20)
                self.show_guest_info(item_values)
            else:
                self.right_frame.pack_forget()
        else:
            self.right_frame.pack_forget()

        #Create Guest function
    def create_guest_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Create Guest")
        popup.geometry("450x600")

        ctk.CTkLabel(popup, text="Create New Guest", font=("Arial", 20, "bold")).pack(pady=(20, 10))

        name_var = tk.StringVar()
        contact_var = tk.StringVar()
        rooms_var = tk.StringVar()
        status_var = tk.StringVar(value="Checked In")

        ctk.CTkLabel(popup, text="First Name:", font=("Arial", 14)).pack(pady=(10, 0))
        first_name_var = tk.StringVar()
        first_name_entry = ctk.CTkEntry(popup, textvariable=first_name_var, width=250)
        first_name_entry.pack()

        ctk.CTkLabel(popup, text="Last Name:", font=("Arial", 14)).pack(pady=(10, 0))
        last_name_var = tk.StringVar()
        last_name_entry = ctk.CTkEntry(popup, textvariable=last_name_var, width=250)
        last_name_entry.pack()

        ctk.CTkLabel(popup, text="Contact Information:", font=("Arial", 14)).pack(pady=(10, 0))
        contact_entry = ctk.CTkEntry(popup, textvariable=contact_var, width=250)
        contact_entry.pack()

        ctk.CTkLabel(popup, text="Email:", font=("Arial", 14)).pack(pady=(10, 0))
        email_var = tk.StringVar()
        email_entry = ctk.CTkEntry(popup, textvariable=email_var, width=250)
        email_entry.pack()

        def on_create():
            popup.destroy()

        # Button Frame for Create and Close buttons
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Create Guest",
            font=("Arial", 16, "bold"),
            width=150,
            height=36,
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Close",
            font=("Arial", 16, "bold"),
            fg_color="#e57373",
            command=on_create,
            width=150,
            height=36
        ).pack(side="left", padx=10, pady=10)



if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Guest List Page")
    app = GuestListPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
