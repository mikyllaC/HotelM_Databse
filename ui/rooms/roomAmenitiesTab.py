import os
import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

from models.room import RoomModel
from utils.helpers import log

class RoomAmenitiesTab(ctk.CTkFrame):
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
        self.action_frame.grid_columnconfigure(0, weight=1)  # search expands
        self.action_frame.grid_columnconfigure(1, weight=0)  # add button stays its natural size

        # Search Frame
        self.search_frame = ctk.CTkFrame(self.action_frame, corner_radius=10, fg_color="transparent")
        self.search_frame.grid(column=0, row=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Search Entry with auto-filter
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.search_amenities())
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:", font=("Roboto Condensed", 14))
        self.search_label.pack(side="left", padx=(0, 10), pady=(0, 0))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by Amenity Name",
                                         font=("Roboto Condensed", 14), textvariable=self.search_var,
                                         width=200, corner_radius=2, border_width=1, border_color=self.BORDER_COLOR)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=(0, 0))

        # Add Amenity Button
        self.add_icon = self.load_icon(icon_file="white_plus.png", size=14)
        self.add_button = ctk.CTkButton(self.action_frame,
                                      text="Add Amenity", font=("Roboto Condensed", 14, "bold"),
                                      fg_color=self.BUTTON_COLOR, width=30, height=25,
                                      hover_color=None, image=self.add_icon,
                                      command=self.add_amenity_popup)
        self.add_button.grid(column=1, row=0, padx=(10, 10), pady=(0, 0), ipady=5, ipadx=5)


        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(0, 10), fill="both", expand=True, anchor="n")

        # Right Frame for usage stats
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2,
                                       border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.4, relheight=1)
        self.right_frame.place_forget()

        # Treeview for displaying amenities
        style = ttk.Style(self.table_frame)
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=45, font=self.TREE_FONT, anchor="w")
        style.map("Treeview",
                 background=[('selected', self.TREE_SELECT_COLOR)],
                 foreground=[('selected', "black")])

        self.treeview = ttk.Treeview(self.table_frame,
                                    columns=["ID", "Amenity Name"],
                                    show="headings")
        self.treeview.pack(expand=True, fill="both", padx=0, pady=0)
        self.treeview.tag_configure('oddrow', background='#f5f5f5')
        self.treeview.tag_configure('evenrow', background='white')

        # Set the column headings and widths
        headings = ["ID", "Amenity Name"]
        for col in headings:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w", width=100, stretch=True)

        self.treeview.column("ID", width=80, anchor="w", stretch=False)
        self.treeview.column("Amenity Name", width=400, anchor="w")

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)


    def populate_treeview(self):
        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        # Get all amenities from database
        amenities = self.room_model.get_all_amenities()

        # Add amenities to treeview
        for i, amenity in enumerate(amenities):
            values = (
                amenity["AMENITY_ID"],
                amenity["AMENITY_NAME"]
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", values=values, tags=(tag,))


    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            item_values = self.treeview.item(selected_item, 'values')
            self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.4, relheight=1)
            self.show_amenity_usage(item_values[0])  # Pass the amenity ID


    def show_amenity_usage(self, amenity_id):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Get amenity details using the model method
        amenity = self.room_model.get_amenity_by_id(amenity_id)
        if not amenity:
            return

        amenity_name = amenity["AMENITY_NAME"]

        # Get room types that use this amenity using the model method
        room_types = self.room_model.get_room_types_for_amenity(amenity_id)

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
                                       command=lambda: self.edit_amenity(amenity_id, amenity_name))
        self.edit_button.grid(column=0, row=0, padx=(0, 5))

        self.delete_button = ctk.CTkButton(right_header_frame, text="Delete", text_color="black", width=50, height=30,
                                       corner_radius=4, fg_color="#ffcccc",
                                       border_width=1, border_color=self.BORDER_COLOR,
                                       command=lambda: self.delete_amenity(amenity_id, amenity_name))
        self.delete_button.grid(column=1, row=0, padx=(0, 5))

        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                   corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                   command=lambda: [self.right_frame.place_forget(),
                                                   self.treeview.selection_remove(self.treeview.selection())],
                                   font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=2, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        # Content in a scrollable frame
        scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))
        scrollable.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text=f"Amenity: {amenity_name}", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Usage Information
        info_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        info_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        info_frame.grid_columnconfigure(0, weight=1)

        # Basic info
        info_label = ctk.CTkLabel(info_frame, text=f"ID: {amenity_id}", font=("Roboto", 14))
        info_label.grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(5, 20))

        # Used by room types section
        if room_types:
            used_label = ctk.CTkLabel(info_frame, text="Used by Room Types:", font=("Roboto", 14, "bold"))
            used_label.grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(0, 10))

            # Create a sub-frame for the room types list
            types_frame = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_2)
            types_frame.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))
            types_frame.grid_columnconfigure(0, weight=1)

            # Add each room type to the list
            for i, (type_id, type_name) in enumerate(room_types):
                room_type_label = ctk.CTkLabel(types_frame, text=f"• {type_name} (ID: {type_id})",
                                              font=("Roboto", 12))
                room_type_label.grid(row=i, column=0, sticky="w", padx=(20, 10), pady=(2, 2))
        else:
            # If not used by any room type
            no_use_label = ctk.CTkLabel(info_frame, text="Not currently used by any room type.",
                                       font=("Roboto", 14, "italic"), text_color="#888888")
            no_use_label.grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(5, 10))


    def add_amenity_popup(self):
        from ui.rooms.addRoomAmenity import AddRoomAmenityFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Room Amenity")
        popup.geometry("480x300")
        popup.grab_set()

        frame = AddRoomAmenityFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)


    def edit_amenity(self, amenity_id, current_name):
        # Simple dialog to edit amenity name
        new_name = ctk.CTkInputDialog(title="Edit Amenity", text=f"Change the name of '{current_name}':")
        new_name = new_name.get_input()

        if new_name and new_name.strip() and new_name.strip() != current_name:
            try:
                self.room_model.update_amenity(amenity_id, new_name.strip())
                self.populate_treeview()
                # Reselect the edited item
                for item in self.treeview.get_children():
                    values = self.treeview.item(item, 'values')
                    if str(values[0]) == str(amenity_id):
                        self.treeview.selection_set(item)
                        self.treeview.see(item)
                        self.show_amenity_usage(amenity_id)
                        break
            except Exception as e:
                log(f"Error editing amenity: {e}")
                messagebox.showerror("Error", f"Could not update amenity: {e}")


    def delete_amenity(self, amenity_id, amenity_name):
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete '{amenity_name}'?\n\n"
                                      f"This will remove it from all room types.")

        if confirm:
            try:
                self.room_model.delete_amenity(amenity_id)
                self.right_frame.place_forget()
                self.populate_treeview()
            except Exception as e:
                log(f"Error deleting amenity: {e}")
                messagebox.showerror("Error", f"Could not delete amenity: {e}")


    def search_amenities(self):
        search_text = self.search_var.get().strip().lower()
        if not search_text:
            self.populate_treeview()
            return

        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Get and filter amenities
        amenities = self.room_model.get_all_amenities()

        # Filter amenities where search text appears as consecutive characters in the name
        filtered_amenities = [a for a in amenities if search_text in a["AMENITY_NAME"].lower()]

        # Add filtered amenities to treeview
        for i, amenity in enumerate(filtered_amenities):
            values = (
                amenity["AMENITY_ID"],
                amenity["AMENITY_NAME"]
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.treeview.insert("", "end", values=values, tags=(tag,))


    def load_icon(self, icon_file, size):
        path = os.path.join(os.path.dirname(__file__), "assets", icon_file)
        if os.path.exists(path):
            try:
                from PIL import Image
                pil = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
                return ctk.CTkImage(light_image=pil, dark_image=pil, size=(size, size))
            except Exception as e:
                log(f"Error loading image {icon_file}: {e}")
                return None
        else:
            log(f"[Error]: {icon_file} not found at {path}!")
            return None


    def refresh_amenities(self, selected_amenity=None):
        """Refresh the amenities list after adding a new amenity"""
        self.populate_treeview()

        # If a selected amenity name is provided, find and select it
        if selected_amenity:
            for item in self.treeview.get_children():
                values = self.treeview.item(item, 'values')
                if values[1] == selected_amenity:  # Amenity name is in the second column
                    self.treeview.selection_set(item)
                    self.treeview.see(item)
                    self.show_amenity_usage(values[0])  # Show details with amenity ID
                    break
