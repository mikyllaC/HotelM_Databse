# ============== Imports ==============
import customtkinter as ctk             # customtkinter
from ui.dashboard import Dashboard      # dashboard screen
from ui.login_screen import LoginScreen # login screen
from utils.helpers import clear_screen, log


def main():
    ctk.set_appearance_mode("light")    # set overall appearance mode: light/dark/system
    ctk.set_default_color_theme("blue") # set default color theme

    app = Application()                 # creates the app
    log(f"Application instance created.")
    app.mainloop()                      # keeps the app running


# ============== Main Application Class ==============
class Application(ctk.CTk):
    def __init__(self):
        log("Application started.")
        super().__init__()              # gives the Application class all the behaviors of a CTk window
        self.title("Hotel Management System")   # set window title
        self.geometry("1600x900")       # set window size (width x height)
        log("Main window initialized with title and geometry.")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.skip_login = False          # ENABLING THIS CAN CAUSE ISSUES AND ERRORS WITH CERTAIN ACTIONS
        if self.skip_login:
            log("[DEV] Login skipped manually.")
            self.on_login_success()     # skip login screen
        else:
            self.show_login_screen()    # show login screen first


    def show_login_screen(self):
        # Displays the login screen
        clear_screen(self)
        self.login_screen = LoginScreen(self, self.on_login_success)
        self.login_screen.pack(fill="both", expand=True) # make it fill the window
        log("Login screen displayed.")


    def on_login_success(self):
        # Displays the dashboard after successful login
        clear_screen(self)
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)
        log("Dashboard displayed.")


    def on_closing(self):
        # Logs out user on application close
        from utils.session import Session

        if Session.current_user:
            log(f"Logging out: [{Session.current_user.get('EMPLOYEE_ID', 'Unknown')}]")
        else:
            log("Logging out: No user currently in session.")
        Session.current_user = None
        log("Application closing.")
        self.destroy()


if __name__ == "__main__":
    main()