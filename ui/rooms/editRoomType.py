import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import shutil

from models.room import RoomModel
from ui.components.customDropdown import CustomDropdown
from utils.helpers import log


class EditRoomTypeFrame(ctk.CTkFrame):
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
    PADX_LABEL = (20, 20)

    def __init__(self, parent_popup, room_type_id, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color=self.BG_COLOR_2)
        self.parent_page = parent_page
        self.room_model = RoomModel()
        self.room_type_id = room_type_id
        self.room_type_data = self.room_model.get_room_type_by_id(room_type_id)

        if not self.room_type_data:
            messagebox.showerror("Error", f"Room type with ID {room_type_id} not found")
            self.master.destroy()
            return

        self.entries = {}
        self.required_fields = ["entry_type_name", "entry_bed_type", "entry_base_adults", "entry_extra_adults",
                                "entry_max_occupancy"]
        self.numeric_fields = ["entry_base_adults", "entry_extra_adults", "entry_max_occupancy"]
        self.bed_types = ["Single", "Double", "Queen", "King", "Twin"]
        self.image_path = self.room_type_data.get("IMAGE")
        self.image_label = None
        self.amenities = []
        self.amenity_map = {}  # Store amenity name -> ID mapping
        self.selected_amenities = []

        # Load amenities and create mapping
        for amenity in self.room_model.get_all_amenities():
            self.amenities.append(amenity['AMENITY_NAME'])
            self.amenity_map[amenity['AMENITY_NAME']] = amenity['AMENITY_ID']

        # Get currently selected amenities for this room type
        self.selected_amenities = self.room_model.get_amenities_for_room_type(room_type_id)

        self.create_widgets()
        self.load_room_type_data()

    def load_room_type_data(self):
        """Load the room type data into the form fields"""
        if not self.room_type_data:
            return

        # Populate entry fields
        self.entries["entry_type_name"].insert(0, self.room_type_data["TYPE_NAME"])
        self.bed_type_dropdown.set(self.room_type_data["BED_TYPE"])
        self.entries["entry_base_adults"].insert(0, str(self.room_type_data["BASE_ADULT_NUM"]))
        self.entries["entry_base_children"].insert(0, str(self.room_type_data["BASE_CHILD_NUM"]))
        self.entries["entry_extra_adults"].insert(0, str(self.room_type_data["EXTRA_ADULT_NUM"]))
        self.entries["entry_extra_children"].insert(0, str(self.room_type_data["EXTRA_CHILD_NUM"]))
        self.entries["entry_max_occupancy"].insert(0, str(self.room_type_data["MAX_OCCUPANCY"]))

        if self.room_type_data.get("DESCRIPTION"):
            self.entries["entry_description"].insert(0, self.room_type_data["DESCRIPTION"])

        # Set image info
        if self.room_type_data.get("IMAGE"):
            self.image_path = self.room_type_data["IMAGE"]
            self.image_label.configure(text=self.image_path)

        # Set selected amenities
        if self.selected_amenities:
            self.amenity_dropdown.set(", ".join(self.selected_amenities))


    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_2, corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text=f"Edit Room Type: {self.room_type_data['TYPE_NAME']}",
                             font=self.FONT_HEADER, text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color=self.SEPERATOR_COLOR, border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Form Frame with 2 Columns ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(50, 20), fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # ========== LEFT FRAME ==========
        left_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,20))

        row = 0

        # ========== Room Type Name ==========
        label = ctk.CTkLabel(left_frame, text="Type Name *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Eg : Standard, Deluxe", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_type_name"] = entry
        row += 1

        # ========== Bed Type ==========
        label = ctk.CTkLabel(left_frame, text="Bed Type *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        self.bed_type_dropdown = CustomDropdown(
            parent=self, parent_frame=left_frame,
            row=row, column=1,
            options=self.bed_types, placeholder="-Select-",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False, add_new_callback=None,
            entry_name="entry_bed_type"
        )
        row += 1

        # ========== Base Number of Adults ==========
        label = ctk.CTkLabel(left_frame, text="Base Adults *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Included adults in base price", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_base_adults"] = entry
        row += 1

        # ========== Base Number of Children ==========
        label = ctk.CTkLabel(left_frame, text="Base Children", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Included children in base price", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_base_children"] = entry
        row += 1

        # ========== Extra Adult Capacity ==========
        label = ctk.CTkLabel(left_frame, text="Extra Adult Capacity *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Max additional adults (extra charge)", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_extra_adults"] = entry
        row += 1

        # ========== Extra Child Capacity ==========
        label = ctk.CTkLabel(left_frame, text="Extra Child Capacity", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Max additional children (extra charge)", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_extra_children"] = entry
        row += 1

        # ========== Max Occupancy ==========
        label = ctk.CTkLabel(left_frame, text="Max Occupancy *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Absolute maximum guests allowed", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_max_occupancy"] = entry
        row += 1


        # ========== RIGHT FRAME ==========
        right_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20,0))

        row = 0

        # ========== Description ==========
        label = ctk.CTkLabel(right_frame, text="Description", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(right_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        self.entries["entry_description"] = entry
        row += 1

        # ========== Image Upload ==========
        label = ctk.CTkLabel(right_frame, text="Image", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        upload_btn = ctk.CTkButton(right_frame, text="Change Image", command=self.upload_image)
        upload_btn.grid(row=row, column=1, sticky="w", padx=(0, 20))
        row += 1
        self.image_label = ctk.CTkLabel(right_frame, text="No image selected", font=("Roboto", 10),
                                        text_color="#888888")
        self.image_label.grid(row=row, column=1, sticky="w", padx=(0, 20))
        row += 1

        # ========== Room Amenities (Multi-select Dropdown) ==========
        label = ctk.CTkLabel(right_frame, text="Room Amenities", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        self.amenity_dropdown = CustomDropdown(
            parent=self, parent_frame=right_frame,
            row=row, column=1,
            options=self.amenities, placeholder="Select amenities...",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=True, add_new_text="Amenity",
            add_new_callback=self.add_room_amenity_popup,
            entry_name="entry_amenities",
            multiselect=True
        )
        row += 1

        # ========== Rate Information Note ==========
        note_frame = ctk.CTkFrame(right_frame, fg_color="#f0f8ff", corner_radius=8)
        note_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=self.PADX_LABEL, pady=20)

        note_label = ctk.CTkLabel(note_frame,
                                 text="Note: Room rates are managed separately in the Room Rates section.\n"
                                      "After updating this room type, check the rates in the\n"
                                      "Room Management → Room Rates tab.",
                                 font=("Roboto", 12),
                                 text_color="#1e40af",
                                 justify="left")
        note_label.pack(padx=15, pady=12)


        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        # ========== Save Button ==========
        self.save_button = ctk.CTkButton(button_frame, text="Save Changes", command=self.on_submit,
                                           height=30, width=120)
        self.save_button.grid(row=0, column=0, padx=(0, 10), sticky="w")
        # ========== Cancel Button ==========
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.master.destroy,
                                          height=30, width=80, fg_color=self.BG_COLOR_2, text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.cancel_button.grid(row=0, column=1, sticky="w")


    def upload_image(self):
        log("Opening file dialog to upload image")
        # Open file dialog to select an image
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        if path:
            log(f"Image selected: {path}")

            # Ensure the uploads directory exists
            uploads_dir = os.path.join(os.path.dirname(__file__), "assets", "uploads")
            # Create the directory if it doesn't exist
            os.makedirs(uploads_dir, exist_ok=True)
            # Copy the file to the uploads directory
            filename = os.path.basename(path)
            dest_path = os.path.join(uploads_dir, filename)

            # If file with same name exists, add a number
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                filename = f"{base}_{counter}{ext}"
                dest_path = os.path.join(uploads_dir, filename)
                counter += 1

            # Copy the file to the destination
            shutil.copy2(path, dest_path)
            self.image_path = filename  # Store only the filename
            self.image_label.configure(text=filename)
        else:
            # If no new image selected, keep the existing one
            pass


    def add_room_amenity_popup(self):
        from ui.rooms.addRoomAmenity import AddRoomAmenityFrame
        log("Opening Add Room Amenity popup")

        popup = ctk.CTkToplevel(self)
        popup.title("Add Room Amenity")
        popup.geometry("480x300")
        popup.grab_set()

        popup = AddRoomAmenityFrame(parent_popup=popup, parent_page=self)
        popup.pack(fill="both", expand=True)


    def validate_form(self):
        log("Validating form fields")
        for field in self.required_fields:
            entry = self.entries.get(field)
            if entry and not entry.get().strip():
                messagebox.showerror("Validation Error",
                                     f"{field.replace('entry_', '')
                                     .replace('_', ' ').title()} is required.")
                return False

        # Validate numeric fields (only if not empty)
        for field in self.numeric_fields:
            entry = self.entries.get(field)
            if entry:
                value_str = entry.get().strip()
                if value_str:  # Only validate if not empty
                    try:
                        value = float(value_str)
                        if value < 0:
                            raise ValueError("Value cannot be negative")
                    except ValueError:
                        messagebox.showerror("Validation Error",
                                             f"{field.replace('entry_', '')
                                             .replace('_', ' ').title()} must be a valid number.")
                        return False

        log("Form validation successful")
        return True

    def on_submit(self):
        if not self.validate_form():
            return

        # Collect data from entries
        updated_room_type_data = {
            "ROOM_TYPE_ID": self.room_type_id,
            "TYPE_NAME": self.entries["entry_type_name"].get().strip(),
            "BED_TYPE": self.bed_type_dropdown.get(),
            "BASE_ADULT_NUM": int(self.entries["entry_base_adults"].get().strip()),
            "BASE_CHILD_NUM": int(self.entries["entry_base_children"].get().strip())
            if self.entries["entry_base_children"].get().strip() else 0,
            "EXTRA_ADULT_NUM": int(self.entries["entry_extra_adults"].get().strip()),
            "EXTRA_CHILD_NUM": int(self.entries["entry_extra_children"].get().strip())
            if self.entries["entry_extra_children"].get().strip() else 0,
            "MAX_OCCUPANCY": int(self.entries["entry_max_occupancy"].get().strip()),
            "DESCRIPTION": self.entries["entry_description"].get().strip(),
            "IMAGE": self.image_path,  # Only filename is stored
        }

        # Get the selected amenities from the dropdown
        selected_amenities = self.amenity_dropdown.get()

        try:
            log(f"[DEBUG] Attempting to update room type with data: {updated_room_type_data}")
            # Update room type in database
            self.room_model.update_room_type(updated_room_type_data)
            log(f"Room type updated successfully with ID: {self.room_type_id}")

            # Handle amenities - first remove all existing mappings
            self.room_model.delete_amenities_for_room_type(self.room_type_id)

            # Then add the new mappings
            if selected_amenities:
                log(f"Updating amenities for room type: {selected_amenities}")

                # If it's a comma-separated string, split it
                if isinstance(selected_amenities, str):
                    amenity_list = [a.strip() for a in selected_amenities.split(',')]
                else:
                    amenity_list = selected_amenities

                # Assign each amenity to the room type
                for amenity_name in amenity_list:
                    if amenity_name in self.amenity_map:
                        amenity_id = self.amenity_map[amenity_name]
                        self.room_model.assign_amenity_to_room_type(self.room_type_id, amenity_id)
                        log(f"Assigned amenity '{amenity_name}' (ID: {amenity_id}) to room type ID: {self.room_type_id}")
                    else:
                        log(f"Warning: Amenity '{amenity_name}' not found in amenity map")

            # Update parent first before showing message
            if self.parent_page:
                if hasattr(self.parent_page, 'refresh_room_types'):
                    self.parent_page.refresh_room_types(selected_type=updated_room_type_data["TYPE_NAME"])

                # Mark related tabs for refresh if parent has room management page
                if hasattr(self.parent_page, 'main_page') and hasattr(self.parent_page.main_page, 'mark_for_refresh'):
                    # When updating a room type, mark rooms and amenities tabs for refresh
                    self.parent_page.main_page.mark_for_refresh('rooms', 'amenities', 'room_rates')

            # Show success message
            messagebox.showinfo("Success",
                              f"Room type '{updated_room_type_data['TYPE_NAME']}' updated successfully!")

            # Focus on parent after message is dismissed
            if self.parent_page and hasattr(self.parent_page, 'master'):
                parent = self.parent_page.master
                # Check if parent has the attributes method (not all widgets do)
                if hasattr(parent, 'attributes'):
                    parent.attributes("-topmost", True)
                    parent.focus_force()
                    parent.after(100, lambda: parent.attributes("-topmost", False))
                elif hasattr(parent, 'focus_force'):
                    # If no attributes method but has focus_force, just use that
                    parent.focus_force()

            # Destroy current window
            self.master.destroy()
        except Exception as e:
            log(f"Error updating room type: {e}")
            messagebox.showerror("Error", f"Failed to update room type: {e}")


    def refresh_amenities(self, selected_amenity=None):
        """Refresh the amenities list after adding a new amenity"""
        self.amenities = []
        self.amenity_map = {}

        for amenity in self.room_model.get_all_amenities():
            self.amenities.append(amenity['AMENITY_NAME'])
            self.amenity_map[amenity['AMENITY_NAME']] = amenity['AMENITY_ID']

        # If you have an amenities dropdown, update it here
        if hasattr(self, 'amenity_dropdown') and hasattr(self.amenity_dropdown, 'set_options'):
            self.amenity_dropdown.set_options(self.amenities)

        # Set the selected amenity if provided
        if selected_amenity and selected_amenity in self.amenities and hasattr(self, 'amenity_dropdown'):
            # Keep existing selections and add the new one
            current = self.amenity_dropdown.get()
            if current:
                if isinstance(current, str):
                    current_list = [a.strip() for a in current.split(',')]
                else:
                    current_list = current

                if selected_amenity not in current_list:
                    current_list.append(selected_amenity)
                    self.amenity_dropdown.set(", ".join(current_list))
            else:
                self.amenity_dropdown.set(selected_amenity)
