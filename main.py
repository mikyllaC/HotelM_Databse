# imports
import customtkinter as ctk             # customtkinter
from ui.dashboard import Dashboard      # dashboard screen
from ui.login_screen import LoginScreen # login screen
from utils.helpers import clear_screen  # clear screen function


def main():
    ctk.set_appearance_mode("light")    # set default theme
    app = Application()                 # creates the app
    app.mainloop()                      # keeps the app running

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1024x738")

        self.current_screen = None      # track the current screen

        self.show_login_screen()        # start with the login screen

    def show_login_screen(self):        # show login screen at app start
        clear_screen(self)
        self.login_screen = LoginScreen(self, self.on_login_success)
        self.login_screen.pack(fill="both", expand=True)

    def on_login_success(self):         # when login is successful, move to dashboard
        clear_screen(self)
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)



if __name__ == "__main__":
    main()