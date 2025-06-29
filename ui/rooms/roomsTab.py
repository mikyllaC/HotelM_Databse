import os
import customtkinter as ctk
from tkinter import ttk, StringVar
from PIL import Image, ImageTk

from models.room import RoomModel
from utils.helpers import log

class RoomsTab(ctk.CTkFrame):
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


    def create_widgets(self):
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(padx=(10, 0), pady=(20, 10), fill="x", anchor="n")
        self.action_frame.grid_columnconfigure(0, weight=1)  # filters/search expand
        self.action_frame.grid_columnconfigure(1, weight=0)  # add button stays its natural size


        # Filter and Search Frame
        self.filter_search_frame = ctk.CTkFrame(self.action_frame, corner_radius=10, fg_color="transparent")
        self.filter_search_frame.grid(column=0, row=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Search Frame
        self.search_frame = ctk.CTkFrame(self.filter_search_frame, fg_color="transparent")
        self.search_frame.pack(side="left", padx=(0, 10), pady=(0, 0), fill="y")

        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.filter_rooms())
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:", font=("Roboto Condensed", 14))
        self.search_label.pack(side="left", padx=(0, 10), pady=(0, 0))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by Room Number",
                                         font=("Roboto Condensed", 14), textvariable=self.search_var,
                                         width=200, corner_radius=2, border_width=1, border_color= self.BORDER_COLOR,)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=(0, 0))

        # # Filter Label
        # self.filter_frame = ctk.CTkFrame(self.filter_search_frame, fg_color="transparent")
        # self.filter_frame.grid(column=1, row=0, padx=(0, 10), pady=(0, 0), sticky="ew")
        #
        # self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filter by Status:",
        #                                  font=("Roboto Condensed", 14))
        # self.filter_label.grid(column=0, row=0, padx=(0, 10), pady=(0, 0))
        #
        # self.status_var = StringVar(value="All")
        # self.status_combobox = ctk.CTkComboBox(self.filter_frame, variable=self.status_var,
        #                                        values=["All", "Available", "Occupied", "Maintenance",
        #                                                "Dirty", "Out of order"],
        #                                        command=lambda x: self.treeview.selection_remove(
        #                                            *self.treeview.get_children()))
        # self.status_combobox.grid(column=1, row=0, padx=(0, 10), pady=(0, 0))
        self.status_var = StringVar(value="All")


        # Add Room Button
        self.add_icon = self.load_icon(icon_file="white_plus.png", size=14)

        self.add_room_button = ctk.CTkButton(self.action_frame,
                                             text="Add Room", font=("Roboto Condensed", 14, "bold"),
                                             fg_color=self.BUTTON_COLOR, width=30, height=25,
                                             hover_color=None,
                                             image=self.add_icon,
                                             command=self.add_room_popup
                                             )
        self.add_room_button.grid(column=1, row=0, padx=(10, 10), pady=(0, 0), ipady=5, ipadx=5)

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(0, 10), fill="both", expand=True, anchor="n")

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.5, relheight=1)
        self.right_frame.place_forget()

        # Treeview for displaying rooms
        style = ttk.Style(self.table_frame)
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=45, font=self.TREE_FONT, anchor="w")
        style.map("Treeview",
                  background=[('selected', self.TREE_SELECT_COLOR)],
                  foreground=[('selected', "black")])

        self.treeview = ttk.Treeview(self.table_frame, columns=["Room Number", "Room Type ID", "Room Type",
                                                                "Floor", "Status", "Notes"],
                                     show="headings")
        self.treeview.pack(expand=True, fill="both", padx=0, pady=0)
        self.treeview.tag_configure('oddrow', background='#f5f5f5')
        self.treeview.tag_configure('evenrow', background='white')

        headings = ["Room Number", "Room Type ID", "Room Type", "Floor", "Status", "Notes"]

        for col in headings:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w", width=100, stretch=True)

        # Set the column widths
        self.treeview.column("Room Number", width=100, anchor="w")
        self.treeview.column("Room Type ID", width=0, anchor="w", stretch=False)  # Hide this column
        self.treeview.column("Room Type", width=200, anchor="w")
        self.treeview.column("Floor", width=50, anchor="w")
        self.treeview.column("Status", width=200, anchor="w")
        self.treeview.column("Notes", width=400, anchor="w")

        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

        # End Commands
        self.populate_treeview()


    def show_room_info(self, room_values):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

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
                                         border_width=1, border_color=self.BORDER_COLOR,
                                         command=lambda: self.edit_room_popup(room_values[1]))
        self.edit_button.grid(column=0, row=0, padx=(0, 5))
        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                    corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                    command=lambda: [self.right_frame.place_forget(),
                                                     self.treeview.selection_remove(self.treeview.selection()),
                                                     setattr(self, 'current_guest_index', None)],
                                    font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=1, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0, )
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))
        scrollable.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Overview", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Room Information
        room_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        room_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Add info rows
        info_rows = [
            ("Room Number", room_values[0]),
            ("Floor", room_values[2]),
            ("Status", room_values[3]),
            ("Notes", room_values[4] if room_values[4] else "N/A")
        ]

        room_frame.grid_columnconfigure(0, minsize=150, weight=1, uniform="info")
        room_frame.grid_columnconfigure(1, minsize=350, weight=1, uniform="info")

        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(room_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew")
            # label_cell.grid_propagate(False)

            # Value "cell" frame
            value_cell = ctk.CTkFrame(room_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR, width=300)
            value_cell.grid(row=index, column=1, sticky="nsew")
            # value_cell.grid_propagate(False)

            # Label text
            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w",
                                      wraplength=140, justify="left")
            label_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Value text
            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                      anchor="w", wraplength=340, justify="left")
            value_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Room Type Section
        title_frame2 = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame2.grid(row=3, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame2.grid_columnconfigure(0, weight=1)

        title_label2 = ctk.CTkLabel(title_frame2, text="Room Type", font=("Roboto Condensed", 18))
        title_label2.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border2 = ctk.CTkFrame(title_frame2, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border2.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Room Type Information
        room_type_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        room_type_frame.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        room_type = self.room_model.get_room_type_by_id(room_values[1])
        # log(f"Room Type ID from selected room: {room_values[1]}")

        if not room_type:
            room_type_id, room_type_name, bed_type = ["Unknown"] * 3
            amenities = []
            amenities_str = "None"
        else:
            room_type_id = room_type["ROOM_TYPE_ID"]
            amenities = self.room_model.get_amenities_for_room_type(room_type_id)
            amenities_str = "\n".join(amenities) if amenities else "None"

        # Define room type info rows properly
        info_rows = [
            ("Type ID", room_type["ROOM_TYPE_ID"] if room_type else "Unknown"),
            ("Type Name", room_type["TYPE_NAME"] if room_type else "Unknown"),
            ("Bed Type", room_type["BED_TYPE"] if room_type else "Unknown"),
            ("Base Adults", room_type["BASE_ADULT_NUM"] if room_type else "Unknown"),
            ("Base Children", room_type.get("BASE_CHILD_NUM", 0) if room_type else "Unknown"),
            ("Extra Adults", room_type.get("EXTRA_ADULT_NUM", 0) if room_type else "Unknown"),
            ("Extra Children", room_type.get("EXTRA_CHILD_NUM", 0) if room_type else "Unknown"),
            ("Max Occupancy", room_type["MAX_OCCUPANCY"] if room_type else "Unknown"),
            ("Base Rate", f"${room_type.get('BASE_RATE', 0):.2f}" if room_type else "Unknown"),
            ("Extra Adult Rate", f"${room_type.get('EXTRA_ADULT_RATE', 0):.2f}" if room_type else "Unknown"),
            ("Extra Child Rate", f"${room_type.get('EXTRA_CHILD_RATE', 0):.2f}" if room_type else "Unknown"),
            ("Description", room_type.get("DESCRIPTION", "N/A") if room_type else "Unknown"),
            ("Image", room_type.get("IMAGE", "None") if room_type else "Unknown"),
            ("Amenities", amenities_str)
        ]

        room_type_frame.grid_columnconfigure(0, minsize=150, weight=1, uniform="info")
        room_type_frame.grid_columnconfigure(1, minsize=350, weight=1, uniform="info")

        # Create labels for each room type information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(room_type_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew")

            # Value "cell" frame
            value_cell = ctk.CTkFrame(room_type_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR, width=300)
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

    def filter_rooms(self):
        """Filter rooms based on search text and selected status"""
        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Get the search query and status filter
        search_query = self.search_var.get().lower().strip()
        status_filter = self.status_var.get()

        # Fetch all rooms from database
        rooms = self.room_model.get_all_rooms()

        # Apply filters
        filtered_rooms = []
        for room in rooms:
            # Skip if status filter is applied and doesn't match
            if status_filter != "All" and room["STATUS"] != status_filter:
                continue

            # Skip if search query doesn't match consecutive characters in room number
            room_number = str(room["ROOM_NUMBER"]).lower()
            if search_query and search_query not in room_number:
                continue

            # Room passed all filters, add to the results
            filtered_rooms.append(room)

        # Populate the treeview with filtered room data
        for i, room in enumerate(filtered_rooms):
            room_type = self.room_model.get_room_type_by_id(room["ROOM_TYPE_ID"])
            room_type_name = room_type["TYPE_NAME"] if room_type else "Unknown"
            status = room["STATUS"]
            notes = room["NOTES"] if room["NOTES"] else "N/A"

            values = (room["ROOM_NUMBER"], room["ROOM_TYPE_ID"], room_type_name, room["FLOOR"], status, notes)
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", iid=room["ROOM_ID"], values=values, tags=(tag,))


    def add_room_popup(self):
        from ui.rooms.addRoom import AddRoomFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Room")
        popup.geometry("575x500")
        popup.grab_set()

        frame = AddRoomFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)

    def edit_room_popup(self, room_id):
        from ui.rooms.editRoom import EditRoomFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Room")
        popup.geometry("575x500")
        popup.grab_set()

        frame = EditRoomFrame(parent_popup=popup, parent_page=self, room_id=room_id)
        frame.pack(fill="both", expand=True)


    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            item_values = self.treeview.item(selected_item, 'values')
            self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.5, relheight=1)
            self.show_room_info(item_values)

    def populate_treeview(self):
        # Clear existing items in the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Fetch all rooms from the database
        rooms = self.room_model.get_all_rooms()

        # Populate the treeview with room data
        for i, room in enumerate(rooms):
            room_type = self.room_model.get_room_type_by_id(room["ROOM_TYPE_ID"])
            room_type_name = room_type["TYPE_NAME"] if room_type else "Unknown"
            status = room["STATUS"]
            notes = room["NOTES"] if room["NOTES"] else "N/A"

            values = (room["ROOM_NUMBER"], room["ROOM_TYPE_ID"], room_type_name, room["FLOOR"], status, notes)
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", iid=room["ROOM_ID"], values=values, tags=(tag,))

        # self.right_frame.place_forget()

    def load_icon(self, icon_file, size):
        path = os.path.join(os.path.dirname(__file__), "assets", icon_file)
        pil = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
        log(f"Found icon path: {path}")

        if os.path.exists(path):  # Check if the file exists
            try:
                return ctk.CTkImage(light_image=pil, dark_image=pil, size=(size, size))
            except Exception as e:
                log(f"Error loading image {icon_file}: {e}")
                return None
        else:
            log(f"[Error]: {icon_file} not found at {path}!")
            return None