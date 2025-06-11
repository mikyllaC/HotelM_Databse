import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from models.guest import GuestModel
from ui.reservations.createReservation import CreateReservation

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
        self.guest_model = GuestModel()
        self.guest_data = [["Guest ID", "Guest Name", "Contact Information", "Status"]]

        self.build_ui()
        self.populate_guest_data()


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


    # Close right frame function
    def close_right_frame(self):
        self.right_frame.pack_forget()


    def show_guest_info(self, guest_info):
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Guest Information":
                continue
            if isinstance(widget, ctk.CTkButton):
                continue
            widget.destroy()

        # Clear existing labels before showing new guest info
        labels = self.guest_data[0]
        extra_info = {
            "Pax": "5",
            "Check-in Date": "2023-10-01",
            "Special Requests": "Late check-in, Vegan meals",
            "Room Type": "Deluxe Suite",
            "Payment Status": "Paid",
        }

        wraplength = 200

        for i, label in enumerate(labels):
            if i < len(guest_info):  # Make sure there's a corresponding value
                value = guest_info[i]
                info_label = ctk.CTkLabel(self.right_frame, text=f"{label}: {value}", font=("Arial", 14),
                                          wraplength=wraplength, justify="left")
                info_label.pack(anchor="w", padx=20, pady=2, fill="x")
            else:
                print(f"Warning: No value found for label {label}")
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
            height=36,
            command=self.create_reservation_popup
        )
        create_reservation_button.pack(side="left", padx=(0, 10))

        # Add Guest Button
        add_guest_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Add Guest",
            font=("Arial", 16, "bold"),
            width=150,
            height=36,
            command=self.add_guest_popup
        )
        add_guest_button.pack(side="left", padx=(0, 10))

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


    def populate_guest_data(self):
        # Fetch guest data from the model
        guest_data = self.guest_model.get_all_guests()

        # If no guests, show a placeholder row
        if not guest_data:
            self.guest_data = [["Guest ID", "Guest Name", "Contact Information", "Status"],
                               ["-", "-", "-", "-"]]
        else:
            # Add the header row to the guest_data
            self.guest_data = [["Guest ID", "Name", "Contact Information", "Status"]] + [
                [row[0], f"{row[1]} {row[2]}", row[3], row[6]] for row in guest_data
            ]

        # Populate the treeview with guest data
        self.update_treeview()


    def filter_table(self):
        search_text = self.search_var.get().lower()
        selected_status = self.filter_var.get()

        filtered_data = [self.guest_data[0]]  # Keep the header row
        for row in self.guest_data[1:]:
            # Ensure row has the expected number of columns
            if len(row) == 4:
                guest_id, name, contact, status = row
                if (search_text in name.lower() or not search_text) and \
                        (selected_status == "All Status" or status == selected_status):
                    filtered_data.append(row)
            else:
                print(f"Skipping row with unexpected number of columns: {row}")
        # Update the treeview with the filtered data
        self.update_treeview(filtered_data)


    def update_treeview(self, data=None):
        if data is None:
            data = self.guest_data
        # Clear existing data in the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        # Populate the treeview with the provided data
        for row in data[1:]:
            self.treeview.insert("", "end", values=row)


    # Function to update payment status window pop up
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


    # Function for guest information window pop up
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

        self.update_treeview()

        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)


    # Function to handle row selection in the table
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


    # Create Reservation function
    def create_reservation_popup(self):
        selected_item = self.treeview.selection()
        guest_info = None # Default to None if no guest is selected

        if selected_item:
            guest_info = self.treeview.item(selected_item[0], "values") # Get the selected guest's info

        popup = ctk.CTkToplevel(self)
        popup.title("Create Reservation")
        popup.geometry("1600x800")
        popup.grab_set()

        frame = CreateReservation(popup, guest_info)
        frame.pack(fill="both", expand=True)


    # Add Guest function
    def add_guest_popup(self):
        from ui.guests.createGuest import AddGuestFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Guest")
        popup.geometry("575x750")
        popup.grab_set()

        frame = AddGuestFrame(popup, self)
        frame.pack(fill="both", expand=True)

        # Refresh the guest list after creating a new guest
        frame.submit_button.configure(command=lambda: [frame.add_guest(), self.populate_guest_data()])



if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Guest List Page")
    app = GuestListPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
