import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

from models.room import RoomModel
from models.guest import GuestModel
from models.reservation import ReservationModel
from ui.components.customDropdown import CustomDropdown
from ui.components.modernDatePicker import ModernDateEntry
from utils.helpers import log


class EditReservation(ctk.CTkFrame):
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

    def __init__(self, parent_popup, reservation_id, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color=self.BG_COLOR_2)
        self.parent_page = parent_page
        self.reservation_id = reservation_id
        self.room_model = RoomModel()
        self.guest_model = GuestModel()
        self.reservation_model = ReservationModel()

        # Import the BillingModel here to avoid circular imports
        from models.billing import BillingModel
        self.billing_model = BillingModel()

        self.entries = {}
        self.required_fields = ["entry_guest", "entry_rooms", "entry_adults", "entry_check_in", "entry_check_out"]

        # Get the current reservation data
        self.current_reservation = self.reservation_model.get_reservation_by_id(reservation_id)
        if not self.current_reservation:
            messagebox.showerror("Error", "Reservation not found!")
            # Schedule window destruction to avoid Tkinter errors
            self.master.after(100, self.master.destroy)
            return

        # Check if the reservation has been paid
        if self.billing_model.is_reservation_paid(reservation_id):
            messagebox.showerror("Cannot Edit", "This reservation cannot be edited because it has already been paid.")
            log(f"Attempted to edit a paid reservation (ID: {reservation_id})")
            # Schedule window destruction to avoid Tkinter errors
            self.master.after(100, self.master.destroy)
            return

        # Get available rooms (including the currently selected room)
        self.rooms = []
        self.room_map = {}
        current_room_id = self.current_reservation.get('ROOM_ID')

        for room in self.room_model.get_all_rooms():
            # Include available rooms and the currently selected room
            if room['STATUS'] == 'Available' or room['ROOM_ID'] == current_room_id:
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

        header = ctk.CTkLabel(header_frame, text=f"Edit Reservation #{self.reservation_id}",
                             font=self.FONT_HEADER, text_color="black")
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

        # Find current guest selection
        current_guest_display = None
        current_guest_id = self.current_reservation.get('GUEST_ID')
        for display, guest_id in self.guest_map.items():
            if guest_id == current_guest_id:
                current_guest_display = display
                break

        self.guest_dropdown = CustomDropdown(
            parent=self, parent_frame=left_frame,
            row=row, column=1,
            options=self.guests, placeholder="Select Guest",
            width=self.ENTRY_WIDTH + 100, height=self.ENTRY_HEIGHT,
            entry_name="entry_guest",
            default_value=current_guest_display
        )
        row += 1

        # ========== Room Selection ==========
        label = ctk.CTkLabel(left_frame, text="Room *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        # Find current room selection
        current_room_display = None
        current_room_id = self.current_reservation.get('ROOM_ID')
        for display, room_id in self.room_map.items():
            if room_id == current_room_id:
                current_room_display = display
                break

        self.room_dropdown = CustomDropdown(
            parent=self, parent_frame=left_frame,
            row=row, column=1,
            options=self.rooms, placeholder="Select Room",
            width=self.ENTRY_WIDTH + 100, height=self.ENTRY_HEIGHT,
            entry_name="entry_rooms",
            default_value=current_room_display
        )
        row += 1

        # ========== Check-In Date ==========
        label = ctk.CTkLabel(left_frame, text="Check-In Date *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        date_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        date_frame.grid(row=row, column=1, sticky="w")

        # Parse current check-in date
        check_in_str = self.current_reservation.get('CHECK_IN_DATE')
        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        except:
            check_in_date = datetime.now().date()

        self.check_in_date = ModernDateEntry(
            date_frame,
            initial_date=check_in_date,
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

        # Parse current check-out date
        check_out_str = self.current_reservation.get('CHECK_OUT_DATE')
        try:
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except:
            check_out_date = (datetime.now() + timedelta(days=1)).date()

        self.check_out_date = ModernDateEntry(
            date_frame,
            initial_date=check_out_date,
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

        # ========== Number of Adults ==========
        label = ctk.CTkLabel(right_frame, text="Adults *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.adults_entry = ctk.CTkEntry(
            right_frame, font=self.FONT_ENTRY_LABEL, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR
        )
        self.adults_entry.grid(row=row, column=1, sticky="w", pady=10)
        self.adults_entry.insert(0, str(self.current_reservation.get('NUMBER_OF_ADULTS', 1)))
        self.entries["entry_adults"] = self.adults_entry
        row += 1

        # ========== Number of Children ==========
        label = ctk.CTkLabel(right_frame, text="Children", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.children_entry = ctk.CTkEntry(
            right_frame, font=self.FONT_ENTRY_LABEL, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR
        )
        self.children_entry.grid(row=row, column=1, sticky="w", pady=10)
        self.children_entry.insert(0, str(self.current_reservation.get('NUMBER_OF_CHILDREN', 0)))
        self.entries["entry_children"] = self.children_entry
        row += 1

        # ========== Status ==========
        label = ctk.CTkLabel(right_frame, text="Status", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        status_options = ["Booked", "Confirmed", "Checked In", "Checked Out"]
        current_status = self.current_reservation.get('STATUS', 'Booked')

        self.status_combobox = ctk.CTkComboBox(
            right_frame, values=status_options, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            font=self.FONT_ENTRY_LABEL, border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR
        )
        self.status_combobox.grid(row=row, column=1, sticky="w", pady=10)
        self.status_combobox.set(current_status)
        self.entries["entry_status"] = self.status_combobox
        row += 1

        # ========== Notes ==========
        label = ctk.CTkLabel(right_frame, text="Notes", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.notes_entry = ctk.CTkTextbox(
            right_frame, width=self.ENTRY_WIDTH, height=80,
            border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
            font=self.FONT_ENTRY_LABEL
        )
        self.notes_entry.grid(row=row, column=1, sticky="w", pady=10)
        current_notes = self.current_reservation.get('NOTES', '')
        if current_notes:
            self.notes_entry.insert("1.0", current_notes)
        self.entries["entry_notes"] = self.notes_entry
        row += 1

        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(20, 30))

        # Save Changes Button
        save_button = ctk.CTkButton(
            button_frame, text="Save Changes", font=("Roboto Condensed", 16, "bold"),
            width=150, height=40, command=self.save_changes
        )
        save_button.pack(side="left", padx=(0, 10))

        # Cancel Button
        cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", font=("Roboto Condensed", 16, "bold"),
            width=100, height=40, fg_color="gray", hover_color="darkgray",
            command=self.cancel_edit
        )
        cancel_button.pack(side="left", padx=(10, 0))

    def save_changes(self):
        """Save the updated reservation data"""
        try:
            # Validate required fields
            if not self.validate_fields():
                return

            # Collect updated data
            updated_data = {}

            # Check if guest has changed
            selected_guest = self.guest_dropdown.get()
            if selected_guest and selected_guest in self.guest_map:
                new_guest_id = self.guest_map[selected_guest]
                if new_guest_id != self.current_reservation.get('GUEST_ID'):
                    updated_data['GUEST_ID'] = new_guest_id

            # Check if room has changed
            selected_room = self.room_dropdown.get()
            if selected_room and selected_room in self.room_map:
                new_room_id = self.room_map[selected_room]
                if new_room_id != self.current_reservation.get('ROOM_ID'):
                    updated_data['ROOM_ID'] = new_room_id

            # Check if dates have changed
            new_check_in = self.check_in_date.get_date().strftime('%Y-%m-%d')
            if new_check_in != self.current_reservation.get('CHECK_IN_DATE'):
                updated_data['CHECK_IN_DATE'] = new_check_in

            new_check_out = self.check_out_date.get_date().strftime('%Y-%m-%d')
            if new_check_out != self.current_reservation.get('CHECK_OUT_DATE'):
                updated_data['CHECK_OUT_DATE'] = new_check_out

            # Check if adults count has changed
            try:
                new_adults = int(self.adults_entry.get())
                if new_adults != self.current_reservation.get('NUMBER_OF_ADULTS'):
                    updated_data['NUMBER_OF_ADULTS'] = new_adults
            except ValueError:
                messagebox.showerror("Error", "Number of adults must be a valid number")
                return

            # Check if children count has changed
            try:
                new_children = int(self.children_entry.get())
                if new_children != self.current_reservation.get('NUMBER_OF_CHILDREN'):
                    updated_data['NUMBER_OF_CHILDREN'] = new_children
            except ValueError:
                messagebox.showerror("Error", "Number of children must be a valid number")
                return

            # Check if status has changed
            new_status = self.status_combobox.get()
            if new_status != self.current_reservation.get('STATUS'):
                updated_data['STATUS'] = new_status

            # Check if notes have changed
            new_notes = self.notes_entry.get("1.0", "end-1c")
            if new_notes != self.current_reservation.get('NOTES', ''):
                updated_data['NOTES'] = new_notes

            # If no changes were made
            if not updated_data:
                messagebox.showinfo("No Changes", "No changes were made to the reservation.")
                return

            # Validate dates
            if 'CHECK_IN_DATE' in updated_data or 'CHECK_OUT_DATE' in updated_data:
                check_in = updated_data.get('CHECK_IN_DATE', self.current_reservation.get('CHECK_IN_DATE'))
                check_out = updated_data.get('CHECK_OUT_DATE', self.current_reservation.get('CHECK_OUT_DATE'))

                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

                if check_out_date <= check_in_date:
                    messagebox.showerror("Error", "Check-out date must be after check-in date")
                    return

            # Update the reservation
            success = self.reservation_model.update_reservation(self.reservation_id, updated_data)

            if success:
                messagebox.showinfo("Success", "Reservation updated successfully!")
                log(f"Updated reservation {self.reservation_id} with data: {updated_data}")

                # Refresh the parent page if available
                if self.parent_page and hasattr(self.parent_page, 'populate_reservations'):
                    self.parent_page.populate_reservations()

                # Close the popup
                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to update reservation. Please try again.")

        except Exception as e:
            log(f"Error updating reservation: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while updating the reservation: {str(e)}")

    def validate_fields(self):
        """Validate required fields"""
        # Check guest selection
        if not self.guest_dropdown.get():
            messagebox.showerror("Error", "Please select a guest")
            return False

        # Check room selection
        if not self.room_dropdown.get():
            messagebox.showerror("Error", "Please select a room")
            return False

        # Check adults count
        try:
            adults = int(self.adults_entry.get())
            if adults < 1:
                messagebox.showerror("Error", "Number of adults must be at least 1")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for adults")
            return False

        # Check children count
        try:
            children = int(self.children_entry.get())
            if children < 0:
                messagebox.showerror("Error", "Number of children cannot be negative")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for children")
            return False

        # Check maximum occupancy
        selected_room = self.room_dropdown.get()
        room_id = self.room_map.get(selected_room)

        if room_id:
            num_adults = int(self.adults_entry.get())
            num_children = int(self.children_entry.get() or 0)
            total_guests = num_adults + num_children

            # Get room data with room type information
            room_data = self.room_model.get_room_data_with_type(room_id)
            if room_data and "MAX_OCCUPANCY" in room_data:
                max_occupancy = room_data["MAX_OCCUPANCY"]

                if total_guests > max_occupancy:
                    messagebox.showerror(
                        "Validation Error",
                        f"The selected room type '{room_data['TYPE_NAME']}' has a maximum occupancy of {max_occupancy}.\n\n"
                        f"You are attempting to book for {total_guests} guests ({num_adults} adults, {num_children} children).\n\n"
                        "Please select a different room type with higher capacity or reduce the number of guests."
                    )
                    return False

        return True

    def cancel_edit(self):
        """Cancel the edit operation"""
        self.master.destroy()
