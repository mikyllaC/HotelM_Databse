import customtkinter as ctk
from tkinter import messagebox

from models.room import RoomModel
from utils.helpers import log


class EditRoomFrame(ctk.CTkFrame):
    FONT_LABEL = ("Roboto", 14)
    FONT_ENTRY = ("Roboto", 10)
    FONT_ENTRY_LABEL = ("Roboto", 12)
    TEXT_COLOR_LABEL = "black"
    TEXT_COLOR_ENTRY = "#818197"
    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    PADX_LABEL = (20, 80)


    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.parent_page = parent_page
        self.room_model = RoomModel()

        self.entries = {}  # Store references to all entry widgets for later access
        self.create_widgets()

    # ============== Widget Creation ==============
    def create_widgets(self):
        pass