import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog

from models.room import RoomModel
from ui.components.customDropdown import CustomDropdown
#from ui.components.multiSelectDropdown import MultiSelectDropdown
from utils.helpers import log


class AddRoomTypeFrame(ctk.CTkFrame):
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

    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color=self.BG_COLOR_2)
        self.parent_page = parent_page
        self.room_model = RoomModel()

        self.entries = {}
        self.required_fields = ["entry_type_name", "entry_bed_type", "entry_base_adults", "entry_extra_adults",
                                "entry_max_occupancy", "entry_base_rate", "entry_extra_adult_charge",
                                "entry_extra_child_charge"]
        self.numeric_fields = ["entry_base_adults", "entry_extra_adults", "entry_max_occupancy",
                               "entry_base_rate", "entry_extra_adult_charge", "entry_extra_child_charge"]
        self.bed_types = ["Single", "Double", "Queen", "King", "Twin"]
        self.image_path = None
        self.image_label = None
        self.amenities = []
        for amenity in self.room_model.get_all_amenities():
            self.amenities.append(amenity['AMENITY_NAME'])

        self.create_widgets()


    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_2, corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Add Room Type", font=self.FONT_HEADER, text_color="black")
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
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="0")
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
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="0")
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

        # ========== Rate fields ==========
        # Base Rate
        label = ctk.CTkLabel(right_frame, text="Base Rate *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Default nightly rate", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_base_rate"] = entry
        row += 1

        # Extra Adult Charge
        label = ctk.CTkLabel(right_frame, text="Extra Adult Charge *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Additional charge per extra adult", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_extra_adult_charge"] = entry
        row += 1

        # Extra Child Charge
        label = ctk.CTkLabel(right_frame, text="Extra Child Charge *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=row, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        frame.grid(row=row, column=1, sticky="w", padx=(0, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Additional charge per extra child", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_extra_child_charge"] = entry
        row += 1

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
        upload_btn = ctk.CTkButton(right_frame, text="Upload Image", command=self.upload_image)
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
            add_new_callback=self.handle_add_new_amenity,
            entry_name="entry_amenities",
            multiselect=True
        )
        row += 1


        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        # ========== Submit Button ==========
        self.submit_button = ctk.CTkButton(button_frame, text="Add", command=self.on_submit,
                                           height=30, width=80)
        self.submit_button.grid(row=0, column=0, padx=(0, 10), sticky="w")
        # ========== Reset Button ==========
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_form,
                                          height=30, width=80, fg_color=self.BG_COLOR_2, text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.reset_button.grid(row=0, column=1, sticky="w")


    def upload_image(self):
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if path:
            self.image_path = path
            self.image_label.configure(text=path.split("/")[-1])
        else:
            self.image_path = None
            self.image_label.configure(text="No image selected")

    def handle_add_new_amenity(self, dropdown):
        new_amenity = simpledialog.askstring("Add New Amenity", "Amenity name:")
        if new_amenity and new_amenity.strip():
            new_amenity = new_amenity.strip()
            if new_amenity not in dropdown.options:
                dropdown.options.append(new_amenity)
                dropdown.selected_values.add(new_amenity)
                dropdown.update_tags()


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
        room_type_data = {
            "TYPE_NAME": self.entries["entry_type_name"].get().strip(),
            "BED_TYPE": self.bed_type_dropdown.get(),
            "BASE_ADULTS": int(self.entries["entry_base_adults"].get().strip()),
            "EXTRA_ADULTS": int(self.entries["entry_extra_adults"].get().strip()),
            "MAX_OCCUPANCY": int(self.entries["entry_max_occupancy"].get().strip()),
            "BASE_RATE": float(self.entries["entry_base_rate"].get().strip()),
            "EXTRA_ADULT_CHARGE": float(self.entries["entry_extra_adult_charge"].get().strip()),
            "EXTRA_CHILD_CHARGE": float(self.entries["entry_extra_child_charge"].get().strip()),
            "DESCRIPTION": self.entries["entry_description"].get().strip(),
            "IMAGE": self.image_path,
            "AMENITIES": self.amenity_dropdown.get()
        }
        try:
            log(f"[DEBUG] Attempting to add room with data: {room_type_data}")
            room_type_id = self.room_model.add_room_type(room_type_data)
            log(f"Room type added successfully with ID: {room_type_id}")

            # Update parent first before showing message
            if self.parent_page:
                self.parent_page.refresh_room_types(selected_type=room_type_data["TYPE_NAME"])

            # Show success message
            messagebox.showinfo("Success", "Room type added successfully!")

            # Focus on parent after message is dismissed
            if self.parent_page and hasattr(self.parent_page.master, "lift"):
                self.parent_page.master.attributes("-topmost", True)
                self.parent_page.master.focus_force()
                self.parent_page.master.after(100, lambda: self.parent_page.master.attributes("-topmost", False))

            # Destroy current window
            self.master.destroy()
        except Exception as e:
            log(f"Error adding room type: {e}")
            messagebox.showerror("Error", f"Failed to add room type: {e}")


    def reset_form(self):
        log("Resetting form fields")
        for entry in self.entries.values():
            if hasattr(entry, "delete"):
                entry.delete(0, "end")
        if hasattr(self, "bed_type_dropdown"):
            self.bed_type_dropdown.set("")

        # Reset image
        self.image_path = None
        if self.image_label:
            self.image_label.configure(text="No image selected")
