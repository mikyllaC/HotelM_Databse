# ============== Imports ==============
import customtkinter as ctk             # customtkinter
from ui.dashboard import Dashboard      # dashboard screen
from ui.login_screen import LoginScreen # login screen
from utils.helpers import clear_screen  # clear screen function


def main():
    ctk.set_appearance_mode("light")    # set overall appearance mode: light/dark/system
    ctk.set_default_color_theme("blue") # set default color theme

    app = Application()                 # creates the app
    app.mainloop()                      # keeps the app running


# ============== Main Application Class ==============
class Application(ctk.CTk):
    def __init__(self):
        super().__init__()              # gives the Application class all the behaviors of a CTk window
        self.title("Hotel Management System")   # set window title
        self.geometry("1024x738")       # set window size (width x height)

        self.skip_login = False

        self.current_screen = None      # track the current screen

        if self.skip_login:
            self.on_login_success()     # skip login screen
        else:
            self.show_login_screen()    # show login screen first


    def show_login_screen(self):
        # Displays the login screen
        clear_screen(self)
        self.login_screen = LoginScreen(self, self.on_login_success)
        self.login_screen.pack(fill="both", expand=True) # make it fill the window


    def on_login_success(self):
        # Displays the dashboard after successful login
        clear_screen(self)
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)


if __name__ == "__main__":
    main()