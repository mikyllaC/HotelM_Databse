import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

ctk.set_appearance_mode("light")


class CreateReservation(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master.title("Create Reservation")
        self.master.geometry("1600x800")
        self.configure(fg_color="#e0e0e0")

        #List
        self.label = ctk.CTkLabel(self, text="Create a New Reservation", 
                                  font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.list_frame = ctk.CTkFrame(self, 
                                       fg_color="#a2a2a2", 
                                       width=1000, 
                                       height=400)
        self.list_frame.pack(anchor = "center", 
                             pady=20, 
                             padx=20, 
                             expand=True, 
                             fill="both")

        #Button
        self.bottom_frame = ctk.CTkFrame(self, 
                                         fg_color="transparent", 
                                         height=100)
        self.bottom_frame.pack(anchor="center", 
                               pady=(10,20), 
                               padx=20, 
                               fill="x")

        self.create_button = ctk.CTkButton(
            self.bottom_frame,
            text="Create Reservation",
            width=200,
            height=40
        )
        self.create_button.pack(side="right", padx=20)

        self.cancel_button = ctk.CTkButton(
            self.bottom_frame,
            text="Cancel",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.master.destroy
            , fg_color="#b0b0b0"
        )
        self.cancel_button.pack(side="right", padx=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = CreateReservation(root)
    app.pack(fill="both", expand=True)
    root.mainloop()