import customtkinter as ctk

class RoomManagementPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Room Management", font=ctk.CTkFont(size=20)).pack(pady=40)