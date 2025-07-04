import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

from models.guest import GuestModel
from ui.reservations.createReservation import CreateReservation
from utils.helpers import log


class GuestListPage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.guest_model = GuestModel()
        self.guest_data = [["Name", "Phone", "Email", "Address", "Status"]]

        self.create_widgets()
        self.populate_guest_data()


    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Guest Management", font=("Roboto Condensed", 28, "bold"),
                                   text_color="#303644")
        title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))

        # Action Bar Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(anchor="n", padx=(35, 0), fill="x")

        # Add Guest Button
        add_guest_button = ctk.CTkButton(
            self.action_frame,
            text="Add Guest",
            font=("Arial", 16, "bold"),
            width=150,
            height=36,
            command=self.add_guest_popup
        )
        add_guest_button.pack(side="left", padx=(0, 10))

        # Search Entry
        self.search_var = StringVar()
        self.search_entry = ctk.CTkEntry(
            self.action_frame,
            width=220,
            height=36,
            placeholder_text="Search guest name...",
            textvariable=self.search_var,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.action_frame,
            width=160,
            height=36,
            values=["All Status", "Checked In", "Checked Out", "Reserved"],
            variable=self.filter_var,
            font=("Arial", 14),
            command=lambda x: self.filter_table()  # Call filter_table when selection changes
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())
        #self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.filter_table())

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(15, 10), fill="both", expand=True, anchor="n")

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2, corner_radius=0,
                                        border_width=1, border_color=self.BORDER_COLOR)
        self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.25, relheight=1)
        #initially hidden
        self.right_frame.place_forget()

        # Treeview for Guest Data
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=25, font=self.TREE_FONT, anchor="w")

        self.treeview = ttk.Treeview(self.table_frame, columns=["Name", "Phone", "Email", "Address", "Status"],
                                     show="headings")
        self.treeview.pack(expand=True, fill="both")

        for col in self.guest_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w")

        # Set the column widths
        self.treeview.column("Name", width=100, anchor="w")
        self.treeview.column("Phone", width=50, anchor="w")
        self.treeview.column("Email", width=150, anchor="w")
        self.treeview.column("Address", width=450, anchor="w")
        self.treeview.column("Status", width=50, anchor="w")

        self.update_treeview()

        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)


    def format_address(self, line1, line2, street, city, state, country):
        parts = [line1, line2, street, city, state, country]
        return ', '.join(part for part in parts if part and part.strip())


    def populate_guest_data(self):
        guest_data = self.guest_model.get_all_guests()

        if not guest_data:
            self.guest_data = [["ID", "Name", "Phone", "Email", "Address", "Status"],
                               ["-", "-", "-", "-", "-", "-"]]
        else:
            self.guest_data = [["ID", "Name", "Phone", "Email", "Address", "Status"]] + [
                [row[0], f"{row[2]} {row[3]}", row[4], row[5],
                 f"{self.format_address(row[6],row[7],row[8],row[9],row[10],row[11])}", row[12]] for row in guest_data
            ]

        self.update_treeview()


    def filter_table(self):
        search_text = self.search_var.get().lower()
        selected_status = self.filter_var.get()

        filtered_data = [self.guest_data[0]]
        for row in self.guest_data[1:]:
            name = row[1].lower() if len(row) > 1 else ""
            status = row[5] if len(row) > 5 else ""

            # Check both search text and status filter
            name_match = search_text in name
            status_match = selected_status == "All Status" or status == selected_status

            if name_match and status_match:
                filtered_data.append(row)

        self.update_treeview(filtered_data)


    def update_treeview(self, data=None):
        if data is None:
            data = self.guest_data

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # process the data excluding the header
        for row in data[1:]:
            guest_id = row[0]  # Implement this method or adjust as needed
            self.treeview.insert("", "end", iid=guest_id, values=row[1:])  # Exclude the ID from the displayed values


    def show_guest_info(self, guest_info):
        # Clear previous widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.current_guest_index = next(
            (i for i, row in enumerate(self.guest_data[1:]) if str(row[0]) == str(guest_info['GUEST_ID'])), None)


        # Header
        self.right_frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                    border_width=1, border_color=self.BORDER_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # Left Header Frame
        left_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        left_header_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")


        # Previous and Next Buttons
        self.current_guest_index = next((i for i, row in enumerate(self.guest_data[1:])
                                         if str(row[0]) == str(guest_info['GUEST_ID'])), None)

        # Define as None so they can be referenced in update_nav_buttons
        previous_button = None
        next_button = None

        def go_to_previous_guest():
            if self.current_guest_index is not None and self.current_guest_index > 0:
                self.current_guest_index -= 1
                guest_id = self.guest_data[self.current_guest_index + 1][0]  # +1 to skip header
                self.treeview.selection_set(guest_id)
                self.treeview.see(guest_id)
                guest_info = self.guest_model.get_guest_by_id(int(guest_id))
                if guest_info:
                    self.show_guest_info(guest_info)
                # Do not call update_nav_buttons here, as the old buttons are destroyed

        def go_to_next_guest():
            if self.current_guest_index is not None and self.current_guest_index < len(self.guest_data) - 2:
                self.current_guest_index += 1
                guest_id = self.guest_data[self.current_guest_index + 1][0]
                self.treeview.selection_set(guest_id)
                self.treeview.see(guest_id)
                guest_info = self.guest_model.get_guest_by_id(int(guest_id))
                if guest_info:
                    self.show_guest_info(guest_info)
                # Do not call update_nav_buttons here, as the old buttons are destroyed

        def update_nav_buttons():
            # Only update state if buttons still exist (i.e., not destroyed)
            if previous_button and next_button:
                if self.current_guest_index is None:
                    previous_button.configure(state="disabled")
                    next_button.configure(state="disabled")
                else:
                    previous_button.configure(state="normal" if self.current_guest_index > 0 else "disabled")
                    next_button.configure(
                        state="normal" if self.current_guest_index < len(self.guest_data) - 2 else "disabled")

        # Previous and Next Buttons
        previous_button = ctk.CTkButton(left_header_frame, text="<", text_color="black", width=30, height=30,
                                        corner_radius=4, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR,
                                        font=("Roboto", 20), command=go_to_previous_guest)
        previous_button.grid(column=0, row=0, padx=(10, 5))

        next_button = ctk.CTkButton(left_header_frame, text=">", text_color="black", width=30, height=30,
                                    corner_radius=4, fg_color=self.BG_COLOR_2,
                                    border_width=1, border_color=self.BORDER_COLOR,
                                    font=("Roboto", 20), command=go_to_next_guest)
        next_button.grid(column=1, row=0, padx=(0, 10))

        update_nav_buttons()


        # Right Header Frame
        right_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        right_header_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="e")

        # Edit and Exit Buttons
        edit_button = ctk.CTkButton(right_header_frame, text="Edit", text_color="black", width=50, height=30,
                                    corner_radius=4, fg_color=self.BG_COLOR_2,
                                    border_width=1, border_color=self.BORDER_COLOR,
                                    command=self.edit_guest_popup)
        edit_button.grid(column=0, row=0, padx=(0, 5))

        # Delete Button - new
        delete_button = ctk.CTkButton(right_header_frame, text="Delete", text_color="white", width=50, height=30,
                                      corner_radius=4, fg_color="#dc3545", hover_color="#c82333",
                                      border_width=1, border_color=self.BORDER_COLOR,
                                      command=self.handle_delete_guest)
        delete_button.grid(column=1, row=0, padx=(0, 5))

        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                    corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                    command=lambda: [self.right_frame.place_forget(),
                                                     self.treeview.selection_remove(self.treeview.selection()),
                                                     setattr(self, 'current_guest_index', None)],
                                    font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=2, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10,0))


        # Title
        title_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Overview", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))


        # Guest Information
        content_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2)
        content_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        full_name = f"{guest_info['FIRST_NAME']} {guest_info['LAST_NAME']}"
        address = self.format_address(
            guest_info.get('ADDRESS_LINE1', ''),
            guest_info.get('ADDRESS_LINE2', ''),
            guest_info.get('STREET', ''),
            guest_info.get('CITY', ''),
            guest_info.get('STATE', ''),
            guest_info.get('COUNTRY', '')
        )

        # Add information rows
        info_rows = [
            ("Guest Id", guest_info['GUEST_ID']),
            ("Name", full_name),
            ("Phone", guest_info['CONTACT_NUMBER']),
            ("Email", guest_info['EMAIL']),
            ("Address", address),
            ("Status", guest_info['STATUS']),
            ("Employee Id", guest_info['EMPLOYEE_ID']),
        ]
        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(content_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew", padx=(0, 0), pady=0)
            #label_cell.grid_columnconfigure(0, weight=1)
            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w")
            label_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Value "cell" frame
            value_cell = ctk.CTkFrame(content_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            value_cell.grid(row=index, column=1, sticky="nsew", padx=(0, 0), pady=0)
            #value_cell.grid_columnconfigure(0, weight=1)
            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                      anchor="w", wraplength=250, justify="left")
            value_text.pack(fill="both", expand=True, padx=10, pady=10)

        content_frame.grid_columnconfigure((0, 1), weight=1, uniform="info")


    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            guest_id = selected_item[0]
            guest_info = self.guest_model.get_guest_by_id(int(guest_id))
            #log(f"Selected Guest ID: {guest_id}, Info: {guest_info}")
            if guest_info:
                self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.4, relheight=1)
                self.show_guest_info(guest_info)
        else:
            self.right_frame.place_forget()


    def add_guest_popup(self):
        from ui.guests.addGuest import AddGuestFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Guest")
        popup.geometry("575x750")
        popup.grab_set()

        frame = AddGuestFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)


    def edit_guest_popup(self):
        from ui.guests.editGuest import EditGuestFrame

        selected_item = self.treeview.selection()
        if selected_item:
            guest_id = int(selected_item[0])

            popup = ctk.CTkToplevel(self)
            popup.title("Edit Guest")
            popup.geometry("575x750")
            popup.grab_set()

            frame = EditGuestFrame(parent_popup=popup, parent_page=self, guest_id=guest_id)
            frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("No Selection", "Please select a guest to edit.")
            log("Edit Guest: No guest selected for editing.")


    def handle_delete_guest(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a guest to delete.")
            return

        guest_id = selected_item[0]
        guest_info = self.guest_model.get_guest_by_id(int(guest_id))

        if guest_info:
            confirm = messagebox.askyesno("Confirm Delete",
                                           f"Are you sure you want to delete guest '{guest_info['FIRST_NAME']} {guest_info['LAST_NAME']}'?",
                                           icon="warning")
            if confirm:
                # Call the delete method and get success status and message
                success, message = self.guest_model.delete_guest(int(guest_id))

                if success:
                    # Only if deletion was successful
                    self.populate_guest_data()
                    self.right_frame.place_forget()
                    messagebox.showinfo("Deleted", "Guest deleted successfully.")
                else:
                    # Show error message with the reason deletion failed
                    messagebox.showerror("Cannot Delete Guest", message)
        else:
            messagebox.showerror("Error", "Guest not found.")


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Guest List Page")
    app = GuestListPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
