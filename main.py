# imports
import tkinter as tk                #base tkinter
import customtkinter as ctk         #customtkinter
from PIL import Image, ImageTk      #use this to resize images if we add later on

# code imports
from ui.dashboard import Dashboard
from ui.login_screen import LoginScreen


def main():
    ctk.set_appearance_mode("light")

    app = Application()
    app.mainloop()


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1024x738")

        self.init_app()

    def init_app(self):
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)


if __name__ == "__main__":
    main()