import customtkinter as ctk

class StaffMaintenancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Staff and Maintenance", font=ctk.CTkFont(size=20)).pack(pady=40)