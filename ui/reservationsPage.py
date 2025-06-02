import customtkinter as ctk

class ReservationsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Reservations", font=ctk.CTkFont(size=20)).pack(pady=40)