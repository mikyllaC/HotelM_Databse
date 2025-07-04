import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar
from datetime import datetime, date

from models.billing import BillingModel
from models.room import RoomModel
from ui.components.customDropdown import CustomDropdown
from ui.components.modernDatePicker import ModernDateEntry
from utils.helpers import log


class RoomRateManagementFrame(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    FONT_HEADER = ("Roboto Condensed", 20, "bold")
    FONT_LABEL = ("Roboto", 14)
    ENTRY_WIDTH = 200
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    SEPARATOR_COLOR = "#D3D3D3"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)

    # Add missing attributes for CustomDropdown compatibility
    TEXT_COLOR_ENTRY = "#818197"
    TEXT_COLOR_LABEL = "black"

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.billing_model = BillingModel()
        self.room_model = RoomModel()

        self.entries = {}
        self.room_types = []
        self.room_type_map = {}

        # Load room types
        self.load_room_types()

        self.create_widgets()
        self.populate_rates_table()

    def load_room_types(self):
        """Load room types from database"""
        try:
            self.room_types = []
            self.room_type_map = {}

            for room_type in self.room_model.get_all_room_types():
                type_name = room_type['TYPE_NAME']
                self.room_types.append(type_name)
                self.room_type_map[type_name] = room_type['ROOM_TYPE_ID']

            if not self.room_types:
                self.room_types = ["No room types available"]

        except Exception as e:
            log(f"Error loading room types: {str(e)}", "ERROR")
            self.room_types = ["Error loading room types"]

    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_1, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Content area with two sections
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Left side - Add/Edit Rate Form
        self.create_rate_form(content_frame)

        # Right side - Rates Table
        self.create_rates_table(content_frame)

    def create_rate_form(self, parent):
        """Create the form for adding/editing rates"""
        form_frame = ctk.CTkFrame(parent, fg_color=self.BG_COLOR_2, corner_radius=8)
        form_frame.pack(side="left", fill="y", padx=(0, 10), pady=0)
        form_frame.pack_propagate(False)
        form_frame.configure(width=350)

        # Form header
        form_header = ctk.CTkLabel(form_frame, text="Add/Edit Room Rate",
                                  font=("Roboto Condensed", 16, "bold"),
                                  text_color="#303644")
        form_header.pack(pady=(20, 15))

        # Scrollable form content
        form_scroll = ctk.CTkScrollableFrame(form_frame, fg_color=self.BG_COLOR_2)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        row = 0

        # Room Type Selection
        ctk.CTkLabel(form_scroll, text="Room Type *", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        self.room_type_dropdown = CustomDropdown(
            parent=self, parent_frame=form_scroll,
            row=row+1, column=0,
            options=self.room_types, placeholder="Select Room Type",
            width=280, height=self.ENTRY_HEIGHT,
            entry_name="room_type"
        )
        row += 2

        # Rate Name
        ctk.CTkLabel(form_scroll, text="Rate Name *", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        self.rate_name_entry = ctk.CTkEntry(form_scroll, width=280, height=self.ENTRY_HEIGHT,
                                           placeholder_text="e.g., Standard Rate, Holiday Rate")
        self.rate_name_entry.grid(row=row+1, column=0, sticky="w")
        self.entries["rate_name"] = self.rate_name_entry
        row += 2

        # Base Rate
        ctk.CTkLabel(form_scroll, text="Base Rate (₱) *", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        self.base_rate_entry = ctk.CTkEntry(form_scroll, width=280, height=self.ENTRY_HEIGHT,
                                           placeholder_text="0.00")
        self.base_rate_entry.grid(row=row+1, column=0, sticky="w")
        self.entries["base_rate"] = self.base_rate_entry
        row += 2

        # Extra Adult Rate
        ctk.CTkLabel(form_scroll, text="Extra Adult Rate (₱)", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        self.extra_adult_entry = ctk.CTkEntry(form_scroll, width=280, height=self.ENTRY_HEIGHT,
                                             placeholder_text="0.00")
        self.extra_adult_entry.grid(row=row+1, column=0, sticky="w")
        self.entries["extra_adult"] = self.extra_adult_entry
        row += 2

        # Extra Child Rate
        ctk.CTkLabel(form_scroll, text="Extra Child Rate (₱)", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        self.extra_child_entry = ctk.CTkEntry(form_scroll, width=280, height=self.ENTRY_HEIGHT,
                                             placeholder_text="0.00")
        self.extra_child_entry.grid(row=row+1, column=0, sticky="w")
        self.entries["extra_child"] = self.extra_child_entry
        row += 2

        # Effective Date
        ctk.CTkLabel(form_scroll, text="Effective Date *", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        date_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        date_frame.grid(row=row+1, column=0, sticky="w")

        self.effective_date = ModernDateEntry(
            date_frame,
            initial_date=datetime.now().date(),
            date_format='%Y-%m-%d',
            width=280
        )
        self.effective_date.pack()
        self.entries["effective_date"] = self.effective_date
        row += 2

        # Expiry Date (Optional) - Use a simpler approach
        ctk.CTkLabel(form_scroll, text="Expiry Date (Optional)", font=self.FONT_LABEL,
                    text_color="#303644").grid(row=row, column=0, sticky="w", pady=(10, 5))

        # Use a regular entry field for expiry date with placeholder
        self.expiry_date_entry = ctk.CTkEntry(form_scroll, width=280, height=self.ENTRY_HEIGHT,
                                             placeholder_text="YYYY-MM-DD (optional)")
        self.expiry_date_entry.grid(row=row+1, column=0, sticky="w")
        self.entries["expiry_date"] = self.expiry_date_entry
        row += 2

        # Active Status
        self.active_var = ctk.BooleanVar(value=True)
        self.active_checkbox = ctk.CTkCheckBox(form_scroll, text="Active Rate",
                                              variable=self.active_var,
                                              font=self.FONT_LABEL)
        self.active_checkbox.grid(row=row, column=0, sticky="w", pady=(15, 10))
        row += 1

        # Buttons
        button_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        button_frame.grid(row=row, column=0, pady=(20, 10), sticky="w")

        self.save_button = ctk.CTkButton(button_frame, text="Save Rate",
                                        command=self.save_rate,
                                        fg_color="#28a745", hover_color="#218838",
                                        width=130, height=35)
        self.save_button.pack(side="left", padx=(0, 10))

        self.clear_button = ctk.CTkButton(button_frame, text="Clear",
                                         command=self.clear_form,
                                         fg_color="#6c757d", hover_color="#545b62",
                                         width=130, height=35)
        self.clear_button.pack(side="left")

        # Hidden field for editing
        self.editing_rate_id = None

    def create_rates_table(self, parent):
        """Create the rates display table"""
        table_frame = ctk.CTkFrame(parent, fg_color=self.BG_COLOR_2, corner_radius=8)
        table_frame.pack(side="right", fill="both", expand=True, pady=0)

        # Table header
        table_header = ctk.CTkLabel(table_frame, text="Current Room Rates",
                                   font=("Roboto Condensed", 16, "bold"),
                                   text_color="#303644")
        table_header.pack(pady=(20, 15))

        # Search and filter frame
        filter_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Search entry
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_rates())

        search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search rates...",
                                   textvariable=self.search_var, width=200)
        search_entry.pack(side="left", padx=(0, 10))

        # Refresh button
        refresh_button = ctk.CTkButton(filter_frame, text="Refresh",
                                      command=self.populate_rates_table,
                                      width=80, height=30)
        refresh_button.pack(side="right")

        # Treeview for rates
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Configure treeview style
        style = ttk.Style()
        style.configure("Rates.Treeview.Heading", font=self.TREE_HEADER_FONT)
        style.configure("Rates.Treeview", font=self.TREE_FONT, rowheight=30)

        columns = ("Rate Name", "Room Type", "Base Rate", "Extra Adult", "Extra Child",
                  "Effective Date", "Expiry Date", "Status")

        self.rates_tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                      style="Rates.Treeview", height=15)

        # Configure columns
        self.rates_tree.heading("Rate Name", text="Rate Name")
        self.rates_tree.heading("Room Type", text="Room Type")
        self.rates_tree.heading("Base Rate", text="Base Rate (₱)")
        self.rates_tree.heading("Extra Adult", text="Extra Adult (₱)")
        self.rates_tree.heading("Extra Child", text="Extra Child (₱)")
        self.rates_tree.heading("Effective Date", text="Effective Date")
        self.rates_tree.heading("Expiry Date", text="Expiry Date")
        self.rates_tree.heading("Status", text="Status")

        # Configure column widths
        self.rates_tree.column("Rate Name", width=120, anchor="w")
        self.rates_tree.column("Room Type", width=100, anchor="w")
        self.rates_tree.column("Base Rate", width=80, anchor="e")
        self.rates_tree.column("Extra Adult", width=80, anchor="e")
        self.rates_tree.column("Extra Child", width=80, anchor="e")
        self.rates_tree.column("Effective Date", width=100, anchor="center")
        self.rates_tree.column("Expiry Date", width=100, anchor="center")
        self.rates_tree.column("Status", width=70, anchor="center")

        # Pack treeview
        self.rates_tree.pack(side="left", fill="both", expand=True)

        # Configure row colors
        self.rates_tree.tag_configure('active', background='#d4edda')
        self.rates_tree.tag_configure('inactive', background='#f8d7da')
        self.rates_tree.tag_configure('expired', background='#fff3cd')

        # Bind double-click to edit
        self.rates_tree.bind("<Double-1>", self.on_rate_double_click)

    def populate_rates_table(self):
        """Populate the rates table with data from database"""
        # Clear existing items
        for item in self.rates_tree.get_children():
            self.rates_tree.delete(item)

        try:
            # Get all room types and their rates
            room_types = self.room_model.get_all_room_types()

            for room_type in room_types:
                room_type_id = room_type['ROOM_TYPE_ID']
                room_type_name = room_type['TYPE_NAME']

                # Get current rate for this room type
                current_rate = self.billing_model.get_current_room_rate(room_type_id)

                if current_rate:
                    # Convert row to dictionary
                    columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                              "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                              "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                    rate_dict = dict(zip(columns, current_rate))

                    # Determine status and tag
                    is_active = bool(rate_dict['IS_ACTIVE'])
                    expiry_date = rate_dict['EXPIRY_DATE']

                    if not is_active:
                        status = "Inactive"
                        tag = 'inactive'
                    elif expiry_date and datetime.strptime(expiry_date, '%Y-%m-%d').date() < date.today():
                        status = "Expired"
                        tag = 'expired'
                    else:
                        status = "Active"
                        tag = 'active'

                    # Format expiry date
                    expiry_display = expiry_date if expiry_date else "No Expiry"

                    values = (
                        rate_dict['RATE_NAME'],
                        room_type_name,
                        f"₱{float(rate_dict['BASE_RATE']):.2f}",
                        f"₱{float(rate_dict['EXTRA_ADULT_RATE']):.2f}",
                        f"₱{float(rate_dict['EXTRA_CHILD_RATE']):.2f}",
                        rate_dict['EFFECTIVE_DATE'],
                        expiry_display,
                        status
                    )

                    item_id = self.rates_tree.insert("", "end", values=values, tags=(tag,))
                    # Store rate_id for editing
                    self.rates_tree.item(item_id, tags=(tag, f"rate_{rate_dict['RATE_ID']}"))
                else:
                    # No rate set for this room type
                    values = (
                        "No Rate Set",
                        room_type_name,
                        "₱0.00",
                        "₱0.00",
                        "₱0.00",
                        "-",
                        "-",
                        "No Rate"
                    )
                    self.rates_tree.insert("", "end", values=values, tags=('inactive',))

        except Exception as e:
            log(f"Error populating rates table: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not load room rates: {str(e)}")

    def filter_rates(self):
        """Filter rates based on search text"""
        search_text = self.search_var.get().lower()

        # If no search text, show all
        if not search_text:
            self.populate_rates_table()
            return

        # Clear and repopulate with filtered results
        for item in self.rates_tree.get_children():
            self.rates_tree.delete(item)

        try:
            room_types = self.room_model.get_all_room_types()

            for room_type in room_types:
                room_type_id = room_type['ROOM_TYPE_ID']
                room_type_name = room_type['TYPE_NAME']

                current_rate = self.billing_model.get_current_room_rate(room_type_id)

                if current_rate:
                    columns = ["RATE_ID", "ROOM_TYPE_ID", "RATE_NAME", "BASE_RATE",
                              "EXTRA_ADULT_RATE", "EXTRA_CHILD_RATE", "EFFECTIVE_DATE",
                              "EXPIRY_DATE", "IS_ACTIVE", "CREATED_DATE"]
                    rate_dict = dict(zip(columns, current_rate))

                    # Check if this rate matches search
                    if (search_text in rate_dict['RATE_NAME'].lower() or
                        search_text in room_type_name.lower()):

                        # Add to filtered results (same logic as populate_rates_table)
                        is_active = bool(rate_dict['IS_ACTIVE'])
                        expiry_date = rate_dict['EXPIRY_DATE']

                        if not is_active:
                            status = "Inactive"
                            tag = 'inactive'
                        elif expiry_date and datetime.strptime(expiry_date, '%Y-%m-%d').date() < date.today():
                            status = "Expired"
                            tag = 'expired'
                        else:
                            status = "Active"
                            tag = 'active'

                        expiry_display = expiry_date if expiry_date else "No Expiry"

                        values = (
                            rate_dict['RATE_NAME'],
                            room_type_name,
                            f"₱{float(rate_dict['BASE_RATE']):.2f}",
                            f"₱{float(rate_dict['EXTRA_ADULT_RATE']):.2f}",
                            f"₱{float(rate_dict['EXTRA_CHILD_RATE']):.2f}",
                            rate_dict['EFFECTIVE_DATE'],
                            expiry_display,
                            status
                        )

                        item_id = self.rates_tree.insert("", "end", values=values, tags=(tag,))
                        self.rates_tree.item(item_id, tags=(tag, f"rate_{rate_dict['RATE_ID']}"))

        except Exception as e:
            log(f"Error filtering rates: {str(e)}", "ERROR")

    def save_rate(self):
        """Save or update a room rate"""
        try:
            # Validate required fields
            if not self.validate_form():
                return

            # Get selected room type
            room_type_name = self.entries["room_type"].get()
            if room_type_name not in self.room_type_map:
                messagebox.showerror("Error", "Please select a valid room type.")
                return

            room_type_id = self.room_type_map[room_type_name]

            # Get expiry date - handle optional field
            expiry_date_str = self.entries["expiry_date"].get().strip()
            expiry_date = expiry_date_str if expiry_date_str else None

            # Prepare rate data
            rate_data = {
                'RATE_NAME': self.entries["rate_name"].get().strip(),
                'BASE_RATE': float(self.entries["base_rate"].get()),
                'EXTRA_ADULT_RATE': float(self.entries["extra_adult"].get() or 0),
                'EXTRA_CHILD_RATE': float(self.entries["extra_child"].get() or 0),
                'EFFECTIVE_DATE': self.entries["effective_date"].get(),
                'EXPIRY_DATE': expiry_date,
                'IS_ACTIVE': 1 if self.active_var.get() else 0
            }

            if self.editing_rate_id:
                # Update existing rate (from edit mode)
                success = self.billing_model.update_room_rate(self.editing_rate_id, rate_data)
                if success:
                    messagebox.showinfo("Success", "Room rate updated successfully!")
                    self.clear_form()
                    self.populate_rates_table()
                else:
                    messagebox.showerror("Error", "Failed to update room rate.")
            else:
                # Check if a rate already exists for this room type
                existing_rate = self.billing_model.get_room_rate_by_room_type(room_type_id)

                if existing_rate:
                    # Update existing rate
                    success = self.billing_model.update_room_rate(existing_rate['RATE_ID'], rate_data)
                    if success:
                        messagebox.showinfo("Success", "Room rate updated successfully!")
                        self.clear_form()
                        self.populate_rates_table()
                    else:
                        messagebox.showerror("Error", "Failed to update room rate.")
                else:
                    # Add new rate (no existing rate found)
                    rate_id = self.billing_model.add_room_rate(room_type_id, rate_data)
                    if rate_id:
                        messagebox.showinfo("Success", "Room rate added successfully!")
                        self.clear_form()
                        self.populate_rates_table()
                    else:
                        messagebox.showerror("Error", "Failed to add room rate.")

        except ValueError as e:
            messagebox.showerror("Validation Error", "Please enter valid numeric values for rates.")
        except Exception as e:
            log(f"Error saving room rate: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def validate_form(self):
        """Validate form inputs"""
        required_fields = {
            "room_type": "Room Type",
            "rate_name": "Rate Name",
            "base_rate": "Base Rate",
            "effective_date": "Effective Date"
        }

        for field_key, field_name in required_fields.items():
            if field_key == "room_type":
                value = self.entries[field_key].get()
            elif field_key == "effective_date":
                value = self.entries[field_key].get()
            else:
                value = self.entries[field_key].get().strip()

            if not value:
                messagebox.showerror("Validation Error", f"{field_name} is required.")
                return False

        # Validate numeric fields
        try:
            base_rate = float(self.entries["base_rate"].get())
            if base_rate < 0:
                messagebox.showerror("Validation Error", "Base rate cannot be negative.")
                return False

            extra_adult = self.entries["extra_adult"].get()
            if extra_adult and float(extra_adult) < 0:
                messagebox.showerror("Validation Error", "Extra adult rate cannot be negative.")
                return False

            extra_child = self.entries["extra_child"].get()
            if extra_child and float(extra_child) < 0:
                messagebox.showerror("Validation Error", "Extra child rate cannot be negative.")
                return False

        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric values for rates.")
            return False

        # Validate expiry date format if provided
        expiry_date_str = self.entries["expiry_date"].get().strip()
        if expiry_date_str:
            try:
                datetime.strptime(expiry_date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Validation Error", "Expiry date must be in YYYY-MM-DD format.")
                return False

        return True

    def clear_form(self):
        """Clear all form fields"""
        self.entries["rate_name"].delete(0, 'end')
        self.entries["base_rate"].delete(0, 'end')
        self.entries["extra_adult"].delete(0, 'end')
        self.entries["extra_child"].delete(0, 'end')
        self.entries["expiry_date"].delete(0, 'end')

        if hasattr(self.room_type_dropdown, 'clear'):
            self.room_type_dropdown.clear()

        self.active_var.set(True)
        self.editing_rate_id = None
        self.save_button.configure(text="Save Rate")

    def on_rate_double_click(self, event):
        """Handle double-click on rate item"""
        self.edit_selected_rate()

    def edit_selected_rate(self):
        """Edit the selected rate"""
        selection = self.rates_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a rate to edit.")
            return

        item = selection[0]
        item_tags = self.rates_tree.item(item, "tags")

        # Find rate_id from tags
        rate_id = None
        for tag in item_tags:
            if tag.startswith("rate_"):
                try:
                    rate_id = int(tag[5:])
                    break
                except ValueError:
                    continue

        if not rate_id:
            messagebox.showerror("Error", "Could not determine rate ID for editing.")
            return

        # Get rate data and populate form
        try:
            # You'll need to implement a method to get rate by ID
            # For now, we'll extract from the treeview values
            values = self.rates_tree.item(item, "values")

            # Find room type ID
            room_type_name = values[1]
            if room_type_name in self.room_type_map:
                # Populate form with rate data
                self.entries["rate_name"].delete(0, 'end')
                self.entries["rate_name"].insert(0, values[0])

                self.entries["base_rate"].delete(0, 'end')
                self.entries["base_rate"].insert(0, values[2].replace('₱', ''))

                self.entries["extra_adult"].delete(0, 'end')
                self.entries["extra_adult"].insert(0, values[3].replace('₱', ''))

                self.entries["extra_child"].delete(0, 'end')
                self.entries["extra_child"].insert(0, values[4].replace('₱', ''))

                # Set room type dropdown
                if hasattr(self.room_type_dropdown, 'set'):
                    self.room_type_dropdown.set(room_type_name)

                # Set active status
                self.active_var.set(values[7] == "Active")

                self.editing_rate_id = rate_id
                self.save_button.configure(text="Update Rate")

        except Exception as e:
            log(f"Error editing rate: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not load rate for editing: {str(e)}")


    def refresh_data(self):
        """Refresh all data"""
        self.load_room_types()
        if hasattr(self.room_type_dropdown, 'set_options'):
            self.room_type_dropdown.set_options(self.room_types)
        self.populate_rates_table()


# Standalone testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Room Rate Management")
    root.geometry("1200x800")

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    frame = RoomRateManagementFrame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()
