# ============== Imports ==============
import customtkinter as ctk                 # customtkinter
import os
from PIL import Image, ImageTk

from ui.home.homeScreenPage import HomeScreenPage
from ui.rooms.roomManagementPage import RoomManagementPage
from ui.guests.guestListPage import GuestListPage
from ui.reservations.reservationsPage import ReservationsPage
from ui.billing.billingPaymentPage import BillingPaymentPage
from ui.staff.staffMaintenancePage import StaffMaintenancePage
from ui.settings.settingsPage import SettingsPage

from models.auth import AuthModel
from utils.helpers import log


# ============== Dashboard Page ==============
class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pages = {"Home": HomeScreenPage,
                      "Room Management": RoomManagementPage,
                      "Guest Management": GuestListPage,
                      "Reservations": ReservationsPage,
                      "Billing & Payment": BillingPaymentPage,
                      "Staff and Maintenance": StaffMaintenancePage,
                      "Settings": SettingsPage
                      }
        self.current_page = None            # currently active page
        self.buttons = {}                   # store navigation buttons (key: page_name)
        self.icons = {}                     # store icons for each page

        self.load_icons()
        self.create_widgets()               # initialize all ui components


    # ============== Loads Icons ==============
    def load_icons(self):
        icon_files = {
            "Home": "home.png",
            "Room Management": "room.png",
            "Guest Management": "guest.png",
            "Reservations": "reservations.png",
            "Billing & Payment": "billing.png",
            "Staff and Maintenance": "staff.png",
            "Settings": "settings.png",
        }

        for page_name, icon_file in icon_files.items():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "assets", icon_file)
            log(f"Icon path for {page_name}: {icon_path}")
            if os.path.exists(icon_path):  # Check if the file exists
                try:
                    pil_image = Image.open(icon_path).resize((20,20), Image.LANCZOS)
                    self.icons[page_name] = ctk.CTkImage(light_image=pil_image)
                except Exception as e:
                    log(f"Error loading image {icon_file}: {e}")
                    self.icons[page_name] = None
            else:
                log(f"Error: {icon_file} not found at {icon_path}!")
                self.icons[page_name] = None


    # ============== Widget Creation ==============
    def create_widgets(self):
        # ---- Navbar Frame ----
        self.navbar = ctk.CTkFrame(self, corner_radius=0, fg_color="#303644")
        self.navbar.pack(side="top", fill="x")

        # ---- Navbar Title ----
        self.navbarLabel = ctk.CTkLabel(self.navbar,
                                         text="The Reverie Hotel",
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         text_color="#ccc")
        self.navbarLabel.pack(side="left", padx=(15,35))

        # ---- Navigation Buttons ----
        self.button_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        self.button_frame.propagate(True)
        self.button_frame.pack(side="right", fill="both", expand=True)

        for page_name in self.pages:
            icon = self.icons.get(page_name)
            btn = ctk.CTkButton(self.button_frame,
                                text=page_name,
                                font=ctk.CTkFont(family="Roboto", size=14),
                                image=icon,
                                compound="left",  # Icon on the left
                                border_spacing=14,
                                width=0,
                                corner_radius=0,
                                hover_color="#282D38",
                                command=lambda n=page_name: self.select_page(n))
            btn.pack(side="left")
            self.buttons[page_name] = btn  # Store the button in the dictionary

        # ---- Logout Button ----
        # self.logout_button = ctk.CTkButton(self.navbar,
        #                                    text="Log Out",
        #                                    fg_color="#d9534f",      # Bootstrap-style red
        #                                    hover_color="#c9302c",   # Darker red on hover
        #                                    text_color="white",
        #                                    command=self.logout_on_click )
        # self.logout_button.pack(side="right", fill="x", padx=15, pady=10)

        # ---- Select Default Page ----
        self.highlight_button("Home")       # highlight 'Home' button on startup
        self.select_page("Home")            # load home screen by default


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
        for page_name, btn in self.buttons.items():
            if page_name == selected_page:
                btn.configure(fg_color="#20252E", text_color="white")       # Active
            else:
                btn.configure(fg_color="transparent", text_color="#d9d9d9")   # Inactive


    # ============== Logout Handler ==============
    def logout_on_click(self):
        auth = AuthModel()
        auth.logout(self.master)