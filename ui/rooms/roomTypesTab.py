import os
import customtkinter as ctk
from tkinter import ttk, StringVar, messagebox
from PIL import Image, ImageTk

from models.room import RoomModel
from utils.helpers import log

class RoomTypesTab(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)
    TREE_SELECT_COLOR = "#DEECF7"
    BUTTON_COLOR = "#206AA1"

    def __init__(self, parent, main_page):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_2)
        self.main_page = main_page
        self.room_model = RoomModel()

        self.create_widgets()
        self.populate_treeview()


    def create_widgets(self):
        # Action Header Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(padx=(10, 0), pady=(20, 10), fill="x", anchor="n")
        self.action_frame.grid_columnconfigure(0, weight=1)  # filters/search expand
        self.action_frame.grid_columnconfigure(1, weight=0)  # add button stays its natural size

        # Search Frame
        self.search_frame = ctk.CTkFrame(self.action_frame, corner_radius=10, fg_color="transparent")
        self.search_frame.grid(column=0, row=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Search Entry with auto-filter
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.search_room_types())
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:", font=("Roboto Condensed", 14))
        self.search_label.pack(side="left", padx=(0, 10), pady=(0, 0))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by ID or Room Type",
                                         font=("Roboto Condensed", 14), textvariable=self.search_var,
                                         width=200, corner_radius=2, border_width=1, border_color=self.BORDER_COLOR)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=(0, 0))


        # Add Room Type Button
        self.add_icon = self.load_icon(icon_file="white_plus.png", size=14)
        self.add_button = ctk.CTkButton(self.action_frame,
                                       text="Add Room Type", font=("Roboto Condensed", 14, "bold"),
                                       fg_color=self.BUTTON_COLOR, width=30, height=25,
                                       hover_color=None, image=self.add_icon,
                                       command=self.add_room_type_popup)
        self.add_button.grid(column=1, row=0, padx=(10, 10), pady=(0, 0), ipady=5, ipadx=5)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(0, 10), fill="both", expand=True, anchor="n")

        # Right Frame (for room type details)
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.5, relheight=1)
        self.right_frame.place_forget()

        # Treeview for displaying room types
        style = ttk.Style(self.table_frame)
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=45, font=self.TREE_FONT, anchor="w")
        style.map("Treeview",
                  background=[('selected', self.TREE_SELECT_COLOR)],
                  foreground=[('selected', "black")])

        self.treeview = ttk.Treeview(self.table_frame,
                                    columns=["ID", "Type Name", "Bed Type", "Max Occupancy", "Description"],
                                    show="headings")
        self.treeview.pack(expand=True, fill="both", padx=0, pady=0)
        self.treeview.tag_configure('oddrow', background='#f5f5f5')
        self.treeview.tag_configure('evenrow', background='white')

        # Set the column headings and widths
        headings = ["ID", "Type Name", "Bed Type", "Max Occupancy", "Description"]
        for col in headings:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w", width=100, stretch=True)

        # Customize column widths
        self.treeview.column("ID", width=50, anchor="w", stretch=False)
        self.treeview.column("Type Name", width=150, anchor="w")
        self.treeview.column("Bed Type", width=100, anchor="w")
        self.treeview.column("Max Occupancy", width=120, anchor="w")
        self.treeview.column("Description", width=400, anchor="w")

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)


    def populate_treeview(self):
        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        # Get all room types from database
        room_types = self.room_model.get_all_room_types()

        # Add room types to treeview
        for i, room_type in enumerate(room_types):
            values = (
                room_type["ROOM_TYPE_ID"],
                room_type["TYPE_NAME"],
                room_type["BED_TYPE"],
                room_type["MAX_OCCUPANCY"],
                room_type["DESCRIPTION"] if "DESCRIPTION" in room_type.keys() else "N/A"
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", values=values, tags=(tag,))


    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            item_values = self.treeview.item(selected_item, 'values')
            self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.5, relheight=1)
            self.show_room_type_info(item_values[0])  # Pass the room type ID


    def show_room_type_info(self, room_type_id):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Get room type details
        room_type = self.room_model.get_room_type_by_id(int(room_type_id))

        if not room_type:
            return

        # Header
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                    border_width=0, border_color=self.BORDER_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(3, 0))
        header_frame.grid_columnconfigure(0, weight=1)

        # Right Header Frame
        right_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        right_header_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="e")

        # Edit and Exit Buttons
        self.edit_button = ctk.CTkButton(right_header_frame, text="Edit", text_color="black", width=50, height=30,
                                        corner_radius=4, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR)
        self.edit_button.grid(column=0, row=0, padx=(0, 5))
        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                    corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                    command=lambda: [self.right_frame.place_forget(),
                                                     self.treeview.selection_remove(self.treeview.selection())],
                                    font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=1, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Content in a scrollable frame
        scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))
        scrollable.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text=room_type["TYPE_NAME"], font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Room Type Information
        info_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        info_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Get amenities for this room type
        amenities = self.room_model.get_amenities_for_room_type(int(room_type_id))
        amenities_str = "\n".join(amenities) if amenities else "None"

        # Add info rows
        info_rows = [
            ("Type ID", room_type["ROOM_TYPE_ID"]),
            ("Bed Type", room_type["BED_TYPE"]),
            ("Base Adults", room_type["BASE_ADULT_NUM"]),
            ("Base Children", room_type.get("BASE_CHILD_NUM", 0)),
            ("Extra Adults", room_type.get("EXTRA_ADULT_NUM", 0)),
            ("Extra Children", room_type.get("EXTRA_CHILD_NUM", 0)),
            ("Max Occupancy", room_type["MAX_OCCUPANCY"]),
            ("Description", room_type.get("DESCRIPTION", "N/A")),
            ("Image", room_type.get("IMAGE", "None")),
            ("Amenities", amenities_str)
        ]

        info_frame.grid_columnconfigure(0, minsize=150, weight=1, uniform="info")
        info_frame.grid_columnconfigure(1, minsize=350, weight=1, uniform="info")

        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew")

            # Value "cell" frame
            value_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            value_cell.grid(row=index, column=1, sticky="nsew")

            # Label text
            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w",
                                      wraplength=140, justify="left")
            label_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Value text
            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                      anchor="w", wraplength=340, justify="left")
            value_text.pack(fill="both", expand=True, padx=10, pady=10)

            # If this is the image row and there is an image, try to display it
            if label == "Image" and value and value != "None":
                try:
                    image_path = os.path.join(os.path.dirname(__file__), "assets", "uploads", value)
                    if os.path.exists(image_path):
                        image = Image.open(image_path).resize((300, 200), Image.LANCZOS)
                        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 200))
                        image_label = ctk.CTkLabel(value_cell, image=ctk_image, text="")
                        image_label.pack(padx=10, pady=10)
                except Exception as e:
                    log(f"Error loading image: {e}")

        # Configure the edit button
        self.edit_button.configure(command=lambda: self.edit_room_type_popup(int(room_type_id)))


    def add_room_type_popup(self):
        from ui.rooms.addRoomType import AddRoomTypeFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Room Type")
        popup.geometry("1100x700")
        popup.grab_set()

        frame = AddRoomTypeFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)


    def edit_room_type_popup(self, room_type_id):
        # This would open a popup to edit the room type
        # For now it's just a placeholder
        messagebox.showinfo("Edit Room Type", f"Editing room type with ID {room_type_id}")


    def load_icon(self, icon_file, size):
        path = os.path.join(os.path.dirname(__file__), "assets", icon_file)
        if os.path.exists(path):
            try:
                pil = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
                return ctk.CTkImage(light_image=pil, dark_image=pil, size=(size, size))
            except Exception as e:
                log(f"Error loading image {icon_file}: {e}")
                return None
        else:
            log(f"[Error]: {icon_file} not found at {path}!")
            return None


    def refresh_room_types(self, selected_type=None):
        """Refresh the room types list after adding a new room type"""
        self.populate_treeview()

        # If a selected type is provided, find and select it in the treeview
        if selected_type:
            for item in self.treeview.get_children():
                values = self.treeview.item(item, 'values')
                if values[1] == selected_type:  # Type name is in the second column
                    self.treeview.selection_set(item)
                    self.treeview.see(item)
                    break

    def search_room_types(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.populate_treeview()
            return

        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        # Get all room types from database
        room_types = self.room_model.get_all_room_types()

        # Filter room types based on search term (by ID or Type Name)
        # Looking for consecutive letters in the search term
        filtered_room_types = []
        for room_type in room_types:
            room_id = str(room_type["ROOM_TYPE_ID"]).lower()
            room_name = room_type["TYPE_NAME"].lower()

            # Check if search term appears as consecutive characters in room id or name
            if (search_term in room_id) or (search_term in room_name):
                filtered_room_types.append(room_type)

        # Add filtered room types to treeview
        for i, room_type in enumerate(filtered_room_types):
            values = (
                room_type["ROOM_TYPE_ID"],
                room_type["TYPE_NAME"],
                room_type["BED_TYPE"],
                room_type["MAX_OCCUPANCY"],
                room_type["DESCRIPTION"] if "DESCRIPTION" in room_type.keys() else "N/A"
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", values=values, tags=(tag,))

