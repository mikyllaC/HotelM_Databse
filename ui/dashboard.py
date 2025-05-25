import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent

        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.sidebarLabel = ctk.CTkLabel(self.sidebar, text="The Reverie Hotel",
                                         font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebarLabel.pack(pady=(25, 20))

        self.buttons = []
        self.pages = {
            "Home": HomePage,
            "Room Management": RoomManagementPage,
            "Guest List": GuestListPage,
            "Reservations": ReservationsPage,
            "Billing & Payment": BillingPaymentPage,
            "Staff and Maintenance": StaffMaintenancePage,
            "Settings": SettingsPage,
        }

        for name in self.pages:
            btn = ctk.CTkButton(
                self.sidebar,
                text=name,
                fg_color="transparent",
                hover_color="#838383",
                anchor="w",
                command=lambda n=name: self.select_page(n)
            )
            btn.pack(fill="x", padx=0, pady=(0, 10))
            self.buttons.append((btn, name))

        self.current_page = None
        self.highlight_button("Home")
        self.select_page("Home")

    def highlight_button(self, selected):
        for btn, name in self.buttons:
            btn.configure(fg_color="#4a48df" if name == selected else "transparent")

    def select_page(self, page_name):
        self.highlight_button(page_name)
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()
        page_class = self.pages.get(page_name)
        self.current_page = page_class(self)
        self.current_page.pack(side="left", fill="both", expand=True)


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Homepage", font=ctk.CTkFont(size=20)).pack(pady=40)

class RoomManagementPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Room Management", font=ctk.CTkFont(size=20)).pack(pady=40)

class GuestListPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Guest List", font=ctk.CTkFont(size=20)).pack(pady=40)

class ReservationsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Reservations", font=ctk.CTkFont(size=20)).pack(pady=40)

class BillingPaymentPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Billing & Payment", font=ctk.CTkFont(size=20)).pack(pady=40)

class StaffMaintenancePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Staff and Maintenance", font=ctk.CTkFont(size=20)).pack(pady=40)

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=20)).pack(pady=40)