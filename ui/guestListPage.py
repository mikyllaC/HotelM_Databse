import customtkinter as ctk

class GuestListPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Guest List", font=ctk.CTkFont(size=20)).pack(pady=40)