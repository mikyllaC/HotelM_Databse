from tkinter import ttk, StringVar
import customtkinter as ctk
import os
from PIL import Image, ImageTk

from models.room import RoomModel
from utils.helpers import log
from ui.rooms.roomsTab import RoomsTab
from ui.rooms.roomTypesTab import RoomTypesTab
from ui.rooms.roomAmenitiesTab import RoomAmenitiesTab


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

        self.rooms_tab = RoomsTab
        self.room_types_tab = RoomTypesTab
        self.amenities_tab = RoomAmenitiesTab

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

        # Create tabs using external frames
        self.rooms_tab = RoomsTab(self.notebook, self)
        self.room_types_tab = RoomTypesTab(self.notebook, self)
        self.amenities_tab = RoomAmenitiesTab(self.notebook, self)

        # Adding tabs to the notebook
        self.notebook.add(self.rooms_tab, text='Rooms')
        self.notebook.add(self.room_types_tab, text='Room Types')
        self.notebook.add(self.amenities_tab, text='Room Amenities')

        # Populate each tab
        # self.populate_rooms_tab()
        # self.populate_room_types_tab()
        # self.populate_amenities_tab()


    def populate_rooms_tab(self):
        pass



    def populate_room_types_tab(self):
        pass


    def populate_amenities_tab(self):
        # title_label = ctk.CTkLabel(self.amenities_tab, text="Room Amenities", font=("Roboto Condensed", 28, "bold"),
        #                            text_color=self.TITLE_COLOR)
        # title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))
        pass



if __name__ == "__main__":
    root = ctk.CTk()
    app = RoomManagementPage(root)
    root.title("Room Management")
    app.pack(fill="both",
             expand=True)
    root.mainloop()