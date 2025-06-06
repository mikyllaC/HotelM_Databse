import customtkinter as ctk

class BillingPaymentPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Billing & Payment", font=ctk.CTkFont(size=20)).pack(pady=40)