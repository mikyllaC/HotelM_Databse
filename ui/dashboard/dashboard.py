# ============== Imports ==============
import customtkinter as ctk                 # customtkinter'

from ui.home.homeScreenPage import HomeScreenPage
from ui.rooms.roomManagementPage import RoomManagementPage
from ui.guests.guestListPage import GuestListPage
from ui.reservations.reservationsPage import ReservationsPage
from ui.billing.billingPaymentPage import BillingPaymentPage
from ui.staff.staffMaintenancePage import StaffMaintenancePage
from ui.settings.settingsPage import SettingsPage

from models.auth import AuthModel


# ============== Dashboard Page ==============
class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pages = {"Home": HomeScreenPage,
                      "Room Management": RoomManagementPage,
                      "Guest List": GuestListPage,
                      "Reservations": ReservationsPage,
                      "Billing & Payment": BillingPaymentPage,
                      "Staff and Maintenance": StaffMaintenancePage,
                      "Settings": SettingsPage
                      }
        self.current_page = None            # currently active page
        self.buttons = []                   # store navigation buttons

        self.create_widgets()               # initialize all ui components


    # ============== Widget Creation ==============
    def create_widgets(self):
        # Initialize all widgets and layout

        # ---- Sidebar Frame ----
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # ---- Sidebar Title ----
        self.sidebarLabel = ctk.CTkLabel(self.sidebar,
                                         text="The Reverie Hotel",
                                         font=ctk.CTkFont(size=20, weight="bold") )
        self.sidebarLabel.pack(pady=(25, 25), padx=15)

        # ---- Navigation Buttons ----
        for page_name in self.pages:
            btn = ctk.CTkButton(self.sidebar,
                                text=page_name,
                                hover_color="#838383",
                                anchor="w",
                                command=lambda n=page_name: self.select_page(n) )
            # Create sidebar buttons for each page and bind them to open the correct page.
            # We use 'lambda n=name: ...' to capture the current value of 'name' in each loop iteration.
            # Without 'n=name', all buttons would end up using the last value due to late binding in Python.
            # This ensures each button calls 'self.select_page()' with its corresponding page name.
            btn.pack(fill="x", padx=15, pady=(0, 10))
            self.buttons.append((btn, page_name))   # store for later highlight

        # ---- Select Default Page ----
        self.highlight_button("Home")       # highlight 'Home' button on startup
        self.select_page("Home")            # load home screen by default

        # ---- Logout Button ----
        self.logout_button = ctk.CTkButton(self.sidebar,
                                           text="Log Out",
                                           fg_color="#d9534f",      # Bootstrap-style red
                                           hover_color="#c9302c",   # Darker red on hover
                                           text_color="white",
                                           command=self.logout_on_click )
        self.logout_button.pack(side="bottom", fill="x", padx=15, pady=20)


    # ============== Page Selection ==============
    def select_page(self, page_name):
        self.highlight_button(page_name)    # visually highlights the button for the selected page

        if self.current_page:               # destroys the previous page if select_page func gets called
            self.current_page.pack_forget() # removes it visually
            self.current_page.destroy()     # deletes it from memory

        page_screen = self.pages.get(page_name) # get the page class/screen(value) of the page_name(key)

        self.current_page = page_screen(self)   # display the new page screen
        self.current_page.pack(side="left", fill="both", expand=True) # make it fill the remaining space


    # ============== Highlight Active Button ==============
    def highlight_button(self, selected_page):
        for btn, page_name in self.buttons:
            if page_name == selected_page:
                btn.configure(fg_color="#4a48df", text_color="white")       # Active
            else:
                btn.configure(fg_color="transparent", text_color="black")   # Inactive


    # ============== Logout Handler ==============
    def logout_on_click(self):
        auth = AuthModel()
        auth.logout(self.master)