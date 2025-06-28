from tkinter import ttk, StringVar
import customtkinter as ctk
import os
from PIL import Image, ImageTk

from models.room import RoomModel
from utils.helpers import log


class RoomManagementPage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)
    TREE_SELECT_COLOR = "#DEECF7"
    BUTTON_COLOR = "#206AA1"

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.room_model = RoomModel()

        self.create_widgets()


    def create_widgets(self):
        # Style configuration for Notebook and Tabs
        style = ttk.Style(self)
        style.configure("TNotebook", background=self.BG_COLOR_1, borderwidth=0, tabmargins=[0, 0, 0, 0])
        style.configure("TNotebook.Tab", background=self.BG_COLOR_1, foreground=self.TITLE_COLOR,
                        font=("Roboto Condensed", 16, "bold"), padding=[30, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", self.BG_COLOR_2)],
                  foreground=[("selected", self.TITLE_COLOR)],
                  font=[("selected", ("Roboto Condensed", 16, "bold"))])
        style.layout("TNotebook.Tab", [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])

        notebook_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_1, border_width=self.BORDER_WIDTH,
                                        border_color=self.BORDER_COLOR)
        notebook_frame.pack(expand=True, fill="both", padx=0, pady=0)

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(expand=True, fill="both", padx=0, pady=0)

        # Create tabs
        self.rooms_tab = ctk.CTkFrame(self.notebook, fg_color=self.BG_COLOR_1)
        self.room_types_tab = ctk.CTkFrame(self.notebook, fg_color=self.BG_COLOR_1)
        self.amenities_tab = ctk.CTkFrame(self.notebook, fg_color=self.BG_COLOR_1)

        # Adding tabs to the notebook
        self.notebook.add(self.rooms_tab, text='Rooms')
        self.notebook.add(self.room_types_tab, text='Room Types')
        self.notebook.add(self.amenities_tab, text='Room Amenities')

        # Populate each tab
        self.populate_rooms_tab()
        self.populate_room_types_tab()
        self.populate_amenities_tab()


    def populate_rooms_tab(self):
        # Action Header Frame
        self.action_frame = ctk.CTkFrame(self.rooms_tab, fg_color="transparent")
        self.action_frame.pack(padx=(10, 0), pady=(0, 0), fill="x", anchor="n")
        self.action_frame.grid_columnconfigure(0, weight=1)  # filters/search expand
        self.action_frame.grid_columnconfigure(1, weight=0)  # add button stays its natural size

        # Filter and Search Frame
        self.filter_search_frame = ctk.CTkFrame(self.action_frame, corner_radius=10, fg_color="transparent")

        self.filter_search_frame.grid(column=0, row=0, padx=(10, 0), pady=(10, 10))

        # Filter Label
        self.filter_label = ctk.CTkLabel(self.filter_search_frame, text="Filter by Status:",
                                         font=("Roboto Condensed", 14))
        self.filter_label.grid(column=0, row=0, padx=(0, 10), pady=(0, 0))

        # Status Combobox for filtering
        self.status_var = StringVar(value="All")
        self.status_combobox = ctk.CTkComboBox(self.filter_search_frame, variable=self.status_var,
                                                values=["All", "Available", "Occupied", "Maintenance",
                                                        "Dirty", "Out of order"],
                                                command=lambda x: self.treeview.selection_remove(
                                                    *self.treeview.get_children()))
        self.status_combobox.grid(column=1, row=0, padx=(0, 10), pady=(0, 0))

        # Search Entry and Button
        self.search_entry = ctk.CTkEntry(self.filter_search_frame, placeholder_text="Search by Room Number",
                                          font=("Roboto Condensed", 14))
        self.search_entry.grid(column=2, row=0, padx=(0, 10), pady=(0, 0))
        self.search_button = ctk.CTkButton(self.filter_search_frame, text="Search",
                                           command=lambda: self.treeview.selection_remove(
                                               *self.treeview.get_children()))
        self.search_button.grid(column=3, row=0, padx=(0, 10), pady=(0, 0))

        # Add Room Button
        self.add_icon = self.load_icon(icon_file="white_plus.png", size=14)

        self.add_room_button = ctk.CTkButton(self.action_frame,
                                             text="Add", font=("Roboto Condensed", 14, "bold"),
                                             fg_color=self.BUTTON_COLOR, width=30, height=25,
                                             hover_color=None,
                                             image=self.add_icon
                                             )
        self.add_room_button.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), ipady=5, ipadx=5)


        # Table Frame
        self.table_frame = ctk.CTkFrame(self.rooms_tab, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(15, 10), fill="both", expand=True, anchor="n")

        # Right Frame
        self.right_frame = ctk.CTkFrame(self.rooms_tab, width=300, fg_color=self.BG_COLOR_2,
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
        self.treeview.column("Room Type", width=150, anchor="w")
        self.treeview.column("Floor", width=100, anchor="w")
        self.treeview.column("Status", width=200, anchor="w")
        self.treeview.column("Notes", width=400, anchor="w")


        def show_room_info(room_values):
            for widget in self.right_frame.winfo_children():
                widget.destroy()


            # Header
            self.right_frame.grid_columnconfigure(0, weight=1)
            self.right_frame.grid_rowconfigure(1, weight=1)

            header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                        border_width=0, border_color=self.BORDER_COLOR)
            header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(3,0))
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
                                                         self.treeview.selection_remove(self.treeview.selection()),
                                                         setattr(self, 'current_guest_index', None)],
                                        font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
            exit_button.grid(column=1, row=0, padx=(5, 10))

            # Bottom Header Border
            bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
            bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))


            scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,)
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
                #label_cell.grid_propagate(False)

                # Value "cell" frame
                value_cell = ctk.CTkFrame(room_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                          border_width=1, border_color=self.BORDER_COLOR, width=300)
                value_cell.grid(row=index, column=1, sticky="nsew")
                #value_cell.grid_propagate(False)

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

            room_type_values = self.room_model.get_room_type_by_id(room_values[1])
            # log(f"Room Type ID from selected room: {room_values[1]}")

            if room_type_values:
                room_type_id = room_type_values.get("ROOM_TYPE_ID", "Unknown")
                room_type_name = room_type_values.get("TYPE_NAME", "Unknown")
                bed_type = room_type_values.get("BED_TYPE", "Unknown")
                capacity = room_type_values.get("CAPACITY", "Unknown")
                extra_capacity = room_type_values.get("EXTRA_CAPACITY", "Unknown")
            else:
                room_type_id, room_type_name, bed_type, capacity, extra_capacity = ["Unknown"] * 5

            amenities = self.room_model.get_amenities_for_room_type(room_type_id)

            info_rows = [
                ("Type ID", room_type_id),
                ("Type Name", room_type_name),
                ("Bed Type", bed_type),
                ("Capacity", capacity),
                ("Extra Capacity", extra_capacity),
                ("Base Price", room_type_values.get("BASE_PRICE", "Unknown")),
                ("Description", room_type_values.get("DESCRIPTION", "N/A")),
                ("Image", room_type_values.get("IMAGE", "N/A")),
                ("Room Amenities", "\n".join(amenities)) if amenities else ("Room Amenities", "None")
            ]

            room_type_frame.grid_columnconfigure(0, minsize=150, weight=1, uniform="info")
            room_type_frame.grid_columnconfigure(1, minsize=350, weight=1, uniform="info")

            # Create labels for each room type information row
            for index, (label, value) in enumerate(info_rows):
                # Label "cell" frame
                label_cell = ctk.CTkFrame(room_type_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                          border_width=1, border_color=self.BORDER_COLOR)
                label_cell.grid(row=index, column=0, sticky="nsew")
                #label_cell.grid_propagate(False)

                # Value "cell" frame
                value_cell = ctk.CTkFrame(room_type_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                          border_width=1, border_color=self.BORDER_COLOR, width=300)
                value_cell.grid(row=index, column=1, sticky="nsew")
                #value_cell.grid_propagate(False)

                # Label text
                label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w",
                                          wraplength=140, justify="left")
                label_text.pack(fill="both", expand=True, padx=10, pady=10)

                # Value text
                value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                          anchor="w", wraplength=340, justify="left")
                value_text.pack(fill="both", expand=True, padx=10, pady=10)


                def edit_room_popup():
                    pass

                self.edit_button.configure(command=edit_room_popup)


        def on_row_select(event):
            selected_item = self.treeview.selection()

            if selected_item:
                item_values = self.treeview.item(selected_item, 'values')
                self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.5, relheight=1)
                show_room_info(item_values)

        self.treeview.bind("<<TreeviewSelect>>", on_row_select)


        def add_room_popup():
            from ui.rooms.addRoom import AddRoomFrame

            popup = ctk.CTkToplevel(self)
            popup.title("Add Room")
            popup.geometry("575x500")
            popup.grab_set()

            frame = AddRoomFrame(parent_popup=popup, parent_page=self)
            frame.pack(fill="both", expand=True)

        self.add_room_button.configure(command=add_room_popup)

        # End Commands
        self.populate_treeview()

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



    def populate_room_types_tab(self):
        # title_label = ctk.CTkLabel(self.room_types_tab, text="Room Types", font=("Roboto Condensed", 28, "bold"),
        #                            text_color=self.TITLE_COLOR)
        # title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))
        pass


    def populate_amenities_tab(self):
        # title_label = ctk.CTkLabel(self.amenities_tab, text="Room Amenities", font=("Roboto Condensed", 28, "bold"),
        #                            text_color=self.TITLE_COLOR)
        # title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))
        pass


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



if __name__ == "__main__":
    root = ctk.CTk()
    app = RoomManagementPage(root)
    root.title("Room Management")
    app.pack(fill="both",
             expand=True)
    root.mainloop()