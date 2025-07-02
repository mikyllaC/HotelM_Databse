import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

from models.room import RoomModel
from models.guest import GuestModel
from models.reservation import ReservationModel
from ui.components.customDropdown import CustomDropdown
from ui.components.modernDatePicker import ModernDateEntry
from utils.helpers import log


class CreateReservation(ctk.CTkFrame):
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
        self.room_model = RoomModel()
        self.guest_model = GuestModel()
        self.reservation_model = ReservationModel()

        self.entries = {}
        self.required_fields = ["entry_guest", "entry_rooms", "entry_adults", "entry_check_in", "entry_check_out"]

        # Get available rooms
        self.rooms = []
        self.room_map = {}
        for room in self.room_model.get_all_rooms():
            if room['STATUS'] == 'Available':
                room_data = self.room_model.get_room_data_with_type(room['ROOM_ID'])
                if room_data:
                    room_display = f"{room_data['ROOM_NUMBER']} - {room_data['TYPE_NAME']}"
                    self.rooms.append(room_display)
                    self.room_map[room_display] = room_data['ROOM_ID']

        # Get guests
        self.guests = []
        self.guest_map = {}
        for guest in self.guest_model.get_all_guests():
            guest_display = f"{guest['FIRST_NAME']} {guest['LAST_NAME']} ({guest['EMAIL']})"
            self.guests.append(guest_display)
            self.guest_map[guest_display] = guest['GUEST_ID']

        self.create_widgets()

    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_2, corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Create Reservation", font=self.FONT_HEADER, text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color=self.SEPERATOR_COLOR, border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Main Content Area with Two Columns ==========
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Configure grid columns to have equal width
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # ========== Left Column ==========
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        row = 0

        # ========== Guest Selection ==========
        label = ctk.CTkLabel(left_frame, text="Guest *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.guest_dropdown = CustomDropdown(
            parent=self, parent_frame=left_frame,
            row=row, column=1,
            options=self.guests, placeholder="Select Guest",
            width=self.ENTRY_WIDTH + 100, height=self.ENTRY_HEIGHT,
            add_new_text="Guest", add_new_option=True, add_new_callback=self.add_guest_popup,
            entry_name="entry_guest"
        )
        row += 1

        # ========== Room Selection ==========
        label = ctk.CTkLabel(left_frame, text="Room *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.room_dropdown = CustomDropdown(
            parent=self, parent_frame=left_frame,
            row=row, column=1,
            options=self.rooms, placeholder="Select Room",
            width=self.ENTRY_WIDTH + 100, height=self.ENTRY_HEIGHT,
            entry_name="entry_rooms"
        )
        row += 1

        # ========== Check-In Date ==========
        label = ctk.CTkLabel(left_frame, text="Check-In Date *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        date_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        date_frame.grid(row=row, column=1, sticky="w")

        self.check_in_date = ModernDateEntry(
            date_frame,
            initial_date=datetime.now().date(),
            date_format='%Y-%m-%d',
            width=self.ENTRY_WIDTH + 100
        )
        self.check_in_date.pack(pady=5)
        self.entries["entry_check_in"] = self.check_in_date
        row += 1

        # ========== Check-Out Date ==========
        label = ctk.CTkLabel(left_frame, text="Check-Out Date *", font=self.FONT_LABEL,
                             text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        date_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        date_frame.grid(row=row, column=1, sticky="w")

        tomorrow = datetime.now() + timedelta(days=1)
        self.check_out_date = ModernDateEntry(
            date_frame,
            initial_date=tomorrow.date(),
            date_format='%Y-%m-%d',
            width=self.ENTRY_WIDTH + 100
        )
        self.check_out_date.pack(pady=5)
        self.entries["entry_check_out"] = self.check_out_date
        row += 1

        # ========== Right Column ==========
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        row = 0

        # ========== Adults ==========
        label = ctk.CTkLabel(right_frame, text="Number of Adults", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.adults_dropdown = CustomDropdown(
            parent=self, parent_frame=right_frame,
            row=row, column=1,
            options=[str(i) for i in range(1, 11)], placeholder="Select",
            default_value="1",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            entry_name="entry_adults"
        )
        row += 1

        # ========== Children ==========
        label = ctk.CTkLabel(right_frame, text="Number of Children", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.children_dropdown = CustomDropdown(
            parent=self, parent_frame=right_frame,
            row=row, column=1,
            options=[str(i) for i in range(11)], placeholder="Select",
            default_value="0",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            entry_name="entry_children"
        )
        row += 1

        # ========== Special Requests ==========
        label = ctk.CTkLabel(right_frame, text="Notes / Special Requests", font=self.FONT_LABEL,
                             text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        special_requests_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        special_requests_frame.grid(row=row, column=1, sticky="w", pady=10)

        entry = ctk.CTkTextbox(special_requests_frame, width=self.ENTRY_WIDTH, height=80,
                               fg_color=self.BG_COLOR_2, border_width=self.BORDER_WIDTH,
                               border_color=self.BORDER_COLOR)
        entry.pack()
        self.entries["entry_special_requests"] = entry
        row += 1

        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(20, 40))

        # ========== Create Button ==========
        self.submit_button = ctk.CTkButton(button_frame, text="Create Reservation",
                                           command=self.on_submit, height=35, width=150)
        self.submit_button.grid(row=0, column=0, padx=(0, 10))

        # ========== Cancel Button ==========
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel",
                                           command=self.on_cancel, height=35, width=100,
                                           fg_color=self.BG_COLOR_2, text_color="black",
                                           border_width=1, border_color=self.BORDER_COLOR)
        self.cancel_button.grid(row=0, column=1)

    def add_guest_popup(self):
        from ui.guests.addGuest import AddGuestFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Guest")
        popup.geometry("900x600")
        popup.grab_set()

        add_guest_frame = AddGuestFrame(parent_popup=popup, parent_page=self)
        add_guest_frame.pack(fill="both", expand=True)

    def refresh_guests(self):
        """Refresh the guest dropdown after adding a new guest"""
        self.guests = []
        self.guest_map = {}

        for guest in self.guest_model.get_all_guests():
            guest_display = f"{guest['FIRST_NAME']} {guest['LAST_NAME']} ({guest['EMAIL']})"
            self.guests.append(guest_display)
            self.guest_map[guest_display] = guest['GUEST_ID']

        if hasattr(self, 'guest_dropdown') and hasattr(self.guest_dropdown, 'set_options'):
            self.guest_dropdown.set_options(self.guests)

    def validate_form(self):
        # Check required fields
        for field_name in self.required_fields:
            if field_name in ["entry_check_in", "entry_check_out"]:
                continue  # These are handled separately

            field = self.entries.get(field_name, None)
            if field is None or not field.get():
                messagebox.showerror("Validation Error",
                                     f"{field_name.replace('entry_', '').replace('_', ' ').title()} is required.")
                return False

        # Check dates
        check_in = self.check_in_date.get_date()
        check_out = self.check_out_date.get_date()

        today = datetime.now().date()

        if check_in < today:
            messagebox.showerror("Validation Error", "Check-in date cannot be in the past.")
            return False

        if check_out <= check_in:
            messagebox.showerror("Validation Error", "Check-out date must be after check-in date.")
            return False

        return True

    def on_submit(self):
        if not self.validate_form():
            return

        try:
            # Get selected values
            guest_display = self.entries["entry_guest"].get()
            selected_room = self.entries["entry_rooms"].get()  # This is a single value now

            guest_id = self.guest_map.get(guest_display)
            room_id = self.room_map.get(selected_room)  # Get room ID directly

            if not guest_id:
                messagebox.showerror("Error", "Invalid guest selection.")
                return

            if not room_id:
                messagebox.showerror("Error", "Invalid room selection.")
                return

            # Create reservation data
            reservation_data = {
                "GUEST_ID": guest_id,
                "ROOM_IDS": [room_id],  # Pass single room ID in a list
                "CHECK_IN_DATE": self.check_in_date.get(),
                "CHECK_OUT_DATE": self.check_out_date.get(),
                "NUMBER_OF_ADULTS": int(self.entries["entry_adults"].get()),
                "NUMBER_OF_CHILDREN": int(self.entries["entry_children"].get() or 0),
                "NOTES": self.entries["entry_special_requests"].get("1.0", "end-1c"),
                "STATUS": "Confirmed"  # Default status
            }

            log(f"Creating reservation with data: {reservation_data}")

            # Call model to create reservation
            reservation_id = self.reservation_model.add_reservation(reservation_data)

            if reservation_id:
                messagebox.showinfo("Success", f"Reservation created successfully with ID: {reservation_id}")
                if self.parent_page and hasattr(self.parent_page, 'refresh_data'):
                    self.parent_page.refresh_data()
                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to create reservation.")

        except Exception as e:
            log(f"Error creating reservation: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_cancel(self):
        self.master.destroy()