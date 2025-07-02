from tkinter import ttk, StringVar
import customtkinter as ctk
import os
from PIL import Image, ImageTk

from models.room import RoomModel
from utils.helpers import log
from ui.rooms.roomsTab import RoomsTab
from ui.rooms.roomTypesTab import RoomTypesTab
from ui.rooms.roomAmenitiesTab import RoomAmenitiesTab
from ui.rooms.roomRateManagement import RoomRateManagementFrame


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

        # Track which tabs need refresh
        self.needs_refresh = {
            'rooms': False,
            'room_types': False,
            'amenities': False,
            'room_rates': False
        }

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

        # Create tabs using external frames and pass self as parent for refresh access
        self.rooms_tab = RoomsTab(self.notebook, self)
        self.room_types_tab = RoomTypesTab(self.notebook, self)
        self.amenities_tab = RoomAmenitiesTab(self.notebook, self)
        self.room_rates_tab = RoomRateManagementFrame(self.notebook)

        # Adding tabs to the notebook
        self.notebook.add(self.rooms_tab, text='Rooms')
        self.notebook.add(self.room_types_tab, text='Room Types')
        self.notebook.add(self.amenities_tab, text='Room Amenities')
        self.notebook.add(self.room_rates_tab, text='Room Rates')

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        """Handle tab change events and refresh data if needed"""
        try:
            selected_tab = self.notebook.select()
            tab_index = self.notebook.index(selected_tab)

            # Refresh the selected tab if it needs refresh
            if tab_index == 0 and self.needs_refresh['rooms']:  # Rooms tab
                self.refresh_rooms_tab()
                self.needs_refresh['rooms'] = False
            elif tab_index == 1 and self.needs_refresh['room_types']:  # Room Types tab
                self.refresh_room_types_tab()
                self.needs_refresh['room_types'] = False
            elif tab_index == 2 and self.needs_refresh['amenities']:  # Amenities tab
                self.refresh_amenities_tab()
                self.needs_refresh['amenities'] = False
            elif tab_index == 3 and self.needs_refresh['room_rates']:  # Room Rates tab
                self.refresh_room_rates_tab()
                self.needs_refresh['room_rates'] = False

        except Exception as e:
            log(f"Error in tab change event: {str(e)}", "ERROR")

    def mark_for_refresh(self, *tabs):
        """Mark specific tabs for refresh"""
        for tab in tabs:
            if tab in self.needs_refresh:
                self.needs_refresh[tab] = True

    def refresh_rooms_tab(self):
        """Refresh the rooms tab"""
        try:
            if hasattr(self.rooms_tab, 'populate_treeview'):
                self.rooms_tab.populate_treeview()
            log("Rooms tab refreshed")
        except Exception as e:
            log(f"Error refreshing rooms tab: {str(e)}", "ERROR")

    def refresh_room_types_tab(self):
        """Refresh the room types tab"""
        try:
            if hasattr(self.room_types_tab, 'populate_treeview'):
                self.room_types_tab.populate_treeview()
            log("Room types tab refreshed")
        except Exception as e:
            log(f"Error refreshing room types tab: {str(e)}", "ERROR")

    def refresh_amenities_tab(self):
        """Refresh the amenities tab"""
        try:
            if hasattr(self.amenities_tab, 'populate_treeview'):
                self.amenities_tab.populate_treeview()
            log("Amenities tab refreshed")
        except Exception as e:
            log(f"Error refreshing amenities tab: {str(e)}", "ERROR")

    def refresh_room_rates_tab(self):
        """Refresh the room rates tab"""
        try:
            if hasattr(self.room_rates_tab, 'refresh_data'):
                self.room_rates_tab.refresh_data()
            log("Room rates tab refreshed")
        except Exception as e:
            log(f"Error refreshing room rates tab: {str(e)}", "ERROR")

    def refresh_all_tabs(self):
        """Force refresh all tabs"""
        self.refresh_rooms_tab()
        self.refresh_room_types_tab()
        self.refresh_amenities_tab()
        self.refresh_room_rates_tab()


if __name__ == "__main__":
    root = ctk.CTk()
    app = RoomManagementPage(root)
    root.title("Room Management")
    app.pack(fill="both",
             expand=True)
    root.mainloop()