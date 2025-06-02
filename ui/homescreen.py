# ============== Imports ==============
import customtkinter as ctk  # customtkinter for modern UI


# ============== Home Screen ==============
class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#e6e6e6")
        self.create_widgets()  # initialize UI components

        # ============== UI Setup ==============
    def create_widgets(self):
        # ---- Main Content Frame ----
        self.content_frame = ctk.CTkFrame(self, width=1000, height=720, fg_color="#e6e6e6")
        self.content_frame.place(relwidth=1, relheight=1)

        # ---- Title ----
        self.title_label = ctk.CTkLabel(
            self.content_frame, text="Welcome!",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.place(x=30, y=30)

        # ---- Room Availability Section ----
        self.setup_available_rooms()
        self.setup_occupied_rooms()

        # ---- Analytics Section ----
        self.analytics_label = ctk.CTkLabel(
            self.content_frame, text="Analytics",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.analytics_label.place(x=30, y=340, anchor="nw")

        self.setup_occupancy_data()
        self.setup_most_reserved_rooms()

        # ============== Available Rooms ==============
    def setup_available_rooms(self):
        self.available_frame = ctk.CTkFrame(self.content_frame, width=350, height=250)
        self.available_frame.place(x=25, y=80)

        self.available_rooms_label = ctk.CTkLabel(
            self.available_frame, text="Available Rooms",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.available_rooms_label.place(x=175, y=20, anchor="n")  # center of 350

        self.available_rooms_list = ctk.CTkTextbox(
            self.available_frame, width=320, height=170,
            fg_color=self.available_frame.cget("fg_color"),
            font=ctk.CTkFont(family="Courier", size=14)
        )
        self.available_rooms_list.place(x=15, y=60)

        # Sample data (placeholder)
        available_rooms = [
            {"number": "101", "type": "Single"},
            {"number": "102", "type": "Double"},
            {"number": "103", "type": "Suite"},
        ]

        self.available_rooms_list.insert("end", f"{'Room Number':<15}{' Room Type':<15}\n")
        self.available_rooms_list.insert("end", f"{'=' * 15} {'=' * 15}\n")
        for room in available_rooms:
            self.available_rooms_list.insert("end", f"{room['number']:<15}{room['type']:<15}\n")
        self.available_rooms_list.configure(state="disabled")

    # ============== Occupied Rooms ==============
    def setup_occupied_rooms(self):
        self.occupied_frame = ctk.CTkFrame(self.content_frame, width=350, height=250)
        self.occupied_frame.place(x=400, y=80)

        self.occupied_rooms_label = ctk.CTkLabel(
            self.occupied_frame, text="Occupied Rooms",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.occupied_rooms_label.place(x=175, y=20, anchor="n")

        self.occupied_rooms_list = ctk.CTkTextbox(
            self.occupied_frame, width=320, height=170,
            fg_color=self.occupied_frame.cget("fg_color"),
            font=ctk.CTkFont(family="Courier", size=14)
        )
        self.occupied_rooms_list.place(x=15, y=60)

        # Sample data (placeholder)
        occupied_rooms = [
            {"number": "201", "type": "Single"},
            {"number": "202", "type": "Double"},
            {"number": "203", "type": "Suite"},
        ]

        self.occupied_rooms_list.insert("end", f"{'Room Number':<15}{' Room Type':<15}\n")
        self.occupied_rooms_list.insert("end", f"{'=' * 15} {'=' * 15}\n")
        for room in occupied_rooms:
            self.occupied_rooms_list.insert("end", f"{room['number']:<15}{room['type']:<15}\n")
        self.occupied_rooms_list.configure(state="disabled")

    # ============== Occupancy Percentages ==============
    def setup_occupancy_data(self):
        self.occupancy_frame = ctk.CTkFrame(self.content_frame, width=350, height=250)
        self.occupancy_frame.place(x=25, y=380)

        self.occupancy_label = ctk.CTkLabel(
            self.occupancy_frame, text="Occupancy",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.occupancy_label.place(x=175, y=20, anchor="n")

        # Placeholder analytics
        self.occupied_percent_label = ctk.CTkLabel(
            self.occupancy_frame, text="Occupied Rooms: 60%",
            font=ctk.CTkFont(family="Courier", size=14)
        )
        self.occupied_percent_label.place(x=30, y=80)

        self.available_percent_label = ctk.CTkLabel(
            self.occupancy_frame, text="Available Rooms: 40%",
            font=ctk.CTkFont(family="Courier", size=14)
        )
        self.available_percent_label.place(x=30, y=120)

    # ============== Most Reserved Rooms ==============
    def setup_most_reserved_rooms(self):
        self.most_reserved_frame = ctk.CTkFrame(self.content_frame, width=350, height=250)
        self.most_reserved_frame.place(x=400, y=380)

        self.most_reserved_label = ctk.CTkLabel(
            self.most_reserved_frame, text="Most Reserved Rooms",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.most_reserved_label.place(x=175, y=20, anchor="n")

        self.most_reserved_list = ctk.CTkTextbox(
            self.most_reserved_frame, width=320, height=170,
            fg_color=self.most_reserved_frame.cget("fg_color"),
            font=ctk.CTkFont(family="Courier", size=14)
        )
        self.most_reserved_list.place(x=15, y=60)

        # Sample data (placeholder)
        most_reserved_rooms = [
            {"number": "101", "type": "Single", "reservations": 25},
            {"number": "202", "type": "Double", "reservations": 20},
            {"number": "303", "type": "Suite", "reservations": 18},
        ]

        self.most_reserved_list.insert("end", f"{'Room Number':<12}{'Room Type':<12}{'Reservations':<12}\n")
        self.most_reserved_list.insert("end", f"{'=' * 12} {'=' * 12} {'=' * 12}\n")
        for room in most_reserved_rooms:
            self.most_reserved_list.insert(
                "end", f"{room['number']:<12}{room['type']:<12}{room['reservations']:<12}\n"
            )
        self.most_reserved_list.configure(state="disabled")