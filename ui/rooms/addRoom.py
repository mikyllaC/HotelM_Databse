import customtkinter as ctk
from tkinter import messagebox

from models.hotel import HotelModel
from models.room import RoomModel
from ui.components.customDropdown import CustomDropdown
from utils.helpers import log


class AddRoomFrame(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    FONT_HEADER = ("Roboto Condensed", 24)
    FONT_LABEL = ("Roboto", 14)
    FONT_ENTRY = ("Roboto", 10)
    FONT_ENTRY_LABEL = ("Roboto", 12)
    TEXT_COLOR_LABEL = "black"
    TEXT_COLOR_ENTRY = "#818197"
    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    SEPERATOR_COLOR = "#D3D3D3"
    PADX_LABEL = (20, 80)

    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color=self.BG_COLOR_2)
        self.parent_page = parent_page
        self.hotel_model = HotelModel()
        self.room_model = RoomModel()

        self.entries = {}
        self.required_fields = ["entry_floor", "entry_room_number", "entry_room_type", "entry_status"]
        self.floors = [floor for floor in range(1, self.hotel_model.get_hotel_info(1)["FLOORS"] + 1)]

        self.room_types = []
        self.room_type_map = {}
        for room_type in self.room_model.get_all_room_types():
            self.room_types.append(room_type['TYPE_NAME'])
            self.room_type_map[room_type['TYPE_NAME']] = room_type['ROOM_TYPE_ID']
            # ex: {'Single': 1, 'Double': 2, ...}

        self.create_widgets()

    # ============== Widget Creation ==============
    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self,
                                    fg_color=self.BG_COLOR_2,
                                    corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Add Room", font=self.FONT_HEADER, text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color=self.SEPERATOR_COLOR, border_width=1)
        bottom_border.pack(fill="x", side="bottom")


        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(50, 20), fill="both", expand=True)

        # ========== Floor ==========
        label = ctk.CTkLabel(form_frame, text="Floor *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=0, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        #log(f"[DEBUG] Floors available: {self.floors}")
        self.floor_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=0, column=1,
            options=self.floors, placeholder="-Select-",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False, add_new_callback=None,
            entry_name="entry_floor"
        )

        # ========== Room Number ==========
        label = ctk.CTkLabel(form_frame, text="Room Number *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=1, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="101, 102, ...")
        entry.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_room_number"] = entry

        # ========== Room Type ==========
        label = ctk.CTkLabel(form_frame, text="Room Type *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=2, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        #log(f"[DEBUG] Room types available: {self.room_types}")
        #log(f"[DEBUG] Floor types when creating dropdown: {[type(floor) for floor in self.floors]}")
        self.room_type_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=2, column=1,
            options=self.room_types, placeholder="-Select-",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_text="Type", add_new_option=True, add_new_callback=self.add_room_type_popup,
            entry_name="entry_room_type"
        )

        # ========== Status ==========
        label = ctk.CTkLabel(form_frame, text="Status *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=3, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.status_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=3, column=1,
            options=['Available', 'Occupied', 'Dirty', 'Maintenance', 'Out of order'],
            default_value="Available",
            placeholder="-Select-",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False, add_new_callback=None,
            entry_name="entry_status"
        )

        # ========== Notes ==========
        label = ctk.CTkLabel(form_frame, text="Notes", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=4, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_notes"] = entry


        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=6, column=1, pady=(50, 20), sticky="ew")

        # ========== Submit Button ==========
        self.submit_button = ctk.CTkButton(button_frame, text="Add", command=self.on_submit,
                                           height=30, width=80)
        self.submit_button.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # ========== Rest Button ==========
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_form,
                                          height=30, width=80, fg_color=self.BG_COLOR_2, text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.reset_button.grid(row=0, column=2, sticky="w")


    def add_room_type_popup(self):
        from ui.rooms.addRoomType import AddRoomTypeFrame
        log("Opening Add Room Type popup")

        popup = ctk.CTkToplevel(self)
        popup.title("Add Room Type")
        popup.geometry("1100x700")
        popup.grab_set()

        popup = AddRoomTypeFrame(parent_popup=popup, parent_page=self)
        popup.pack(fill="both", expand=True)


    def check_room_number_exists(self, room_number):
        existing_rooms = self.room_model.get_all_rooms()

        for room in existing_rooms:
            if str(room['ROOM_NUMBER']).strip() == str(room_number).strip():
                return True

        return False

    def validate_form(self):
        if self.check_room_number_exists(self.entries["entry_room_number"].get().strip()):
            messagebox.showerror("Validation Error", "Room number already exists.")
            return False

        # Check if all required fields are filled
        for key, entry in self.entries.items():
            if key in self.required_fields:
                if not entry.get().strip():
                    messagebox.showerror("Validation Error",
                                         f"{key.replace('entry_', '').replace('_', ' ').title()} is required.")
                    return False

        return True

    def on_submit(self):
        if not self.validate_form():
            return

        room_type = self.entries["entry_room_type"].get().strip()
        room_type_id = self.room_type_map[room_type] if room_type in self.room_type_map else None

        # Collect data from entries
        room_data = {
            "FLOOR": self.entries["entry_floor"].get().strip(),
            "ROOM_NUMBER": self.entries["entry_room_number"].get().strip(),
            "ROOM_TYPE_ID": room_type_id,
            "STATUS": self.entries["entry_status"].get().strip(),
            "NOTES": self.entries["entry_notes"].get().strip()
        }
        try:
            log(f"[DEBUG] Attempting to add room with data: {room_data}")
            room_id = self.room_model.add_room(room_data)
            log(f"Room added successfully with ID: {room_id}")

            messagebox.showinfo("Success", "Room added successfully!")

            # Refresh current tab and mark others for refresh
            if self.parent_page:
                self.parent_page.populate_treeview()

                # Mark related tabs for refresh if parent has room management page
                if hasattr(self.parent_page, 'main_page') and hasattr(self.parent_page.main_page, 'mark_for_refresh'):
                    # When adding a room, mark room types and amenities tabs for refresh
                    self.parent_page.main_page.mark_for_refresh('room_types', 'amenities', 'room_rates')

            self.master.destroy()
        except Exception as e:
            log(f"Error adding room: {e}")
            messagebox.showerror("Error", f"Failed to add room: {e}")


    def reset_form(self):
        log("Resetting form fields")
        # Reset all entries
        for key, entry in self.entries.items():
            # If it's a CTkEntry (has delete method)
            if hasattr(entry, "delete") and callable(entry.delete):
                entry.delete(0, "end")
            # If it's your CustomDropdown (has set method)
            elif hasattr(entry, "set") and callable(entry.set):
                if key == "entry_status":
                    entry.set("Available")
                else:
                    entry.set("")

        # Also reset the visible dropdowns if you keep references
        self.floor_dropdown.set("")
        self.room_type_dropdown.set("")
        self.status_dropdown.set("Available")


    def refresh_room_types(self, selected_type=None):
        self.room_types = []
        self.room_type_map = {}
        for room_type in self.room_model.get_all_room_types():
            log(f"[DEBUG] Adding room type: {room_type['TYPE_NAME']} with ID: {room_type['ROOM_TYPE_ID']}")
            self.room_types.append(room_type['TYPE_NAME'])
            self.room_type_map[room_type['TYPE_NAME']] = room_type['ROOM_TYPE_ID']
        # Use set_options to update dropdown options
        if hasattr(self.room_type_dropdown, 'set_options'):
            self.room_type_dropdown.set_options(self.room_types)
        # Set the selected value if provided
        if selected_type and selected_type in self.room_types:
            self.room_type_dropdown.set(selected_type)
        else:
            self.room_type_dropdown.set("")
