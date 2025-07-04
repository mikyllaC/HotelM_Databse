import customtkinter as ctk
import calendar
from datetime import datetime


class ModernDatePicker(ctk.CTkFrame):
    def __init__(self, parent, initial_date=None, callback=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Styling constants
        self.BG_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#3b82f6"
        self.HOVER_COLOR = "#dbeafe"
        self.TEXT_COLOR = "#1f2937"
        self.SECONDARY_TEXT = "#6b7280"
        self.BORDER_COLOR = "#d1d5db"

        self.callback = callback
        self.selected_date = initial_date or datetime.now().date()
        self.display_date = self.selected_date.replace(day=1)  # First day of selected month

        self.configure(fg_color=self.BG_COLOR, corner_radius=12, border_width=1, border_color=self.BORDER_COLOR)

        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        # Header with month/year navigation
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        # Previous month button
        self.prev_btn = ctk.CTkButton(
            header_frame, text="‹", width=30, height=30,
            fg_color=self.ACCENT_COLOR, hover_color="#2563eb",
            font=("Arial", 16, "bold"), corner_radius=6,
            command=self.prev_month
        )
        self.prev_btn.pack(side="left")

        # Month/Year label
        self.month_year_label = ctk.CTkLabel(
            header_frame, text="",
            font=("Segoe UI", 16, "bold"),
            text_color=self.TEXT_COLOR
        )
        self.month_year_label.pack(side="left", expand=True)

        # Next month button
        self.next_btn = ctk.CTkButton(
            header_frame, text="›", width=30, height=30,
            fg_color=self.ACCENT_COLOR, hover_color="#2563eb",
            font=("Arial", 16, "bold"), corner_radius=6,
            command=self.next_month
        )
        self.next_btn.pack(side="right")

        # Days of week header
        days_frame = ctk.CTkFrame(self, fg_color="transparent")
        days_frame.pack(fill="x", padx=15, pady=(0, 5))

        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for day in days:
            day_label = ctk.CTkLabel(
                days_frame, text=day, width=35, height=25,
                font=("Segoe UI", 12, "bold"),
                text_color=self.SECONDARY_TEXT
            )
            day_label.pack(side="left", padx=2)

        # Calendar grid
        self.calendar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.calendar_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create 6x7 grid for calendar days
        self.day_buttons = []
        for week in range(6):
            week_buttons = []
            for day in range(7):
                btn = ctk.CTkButton(
                    self.calendar_frame, text="", width=35, height=35,
                    fg_color="transparent", hover_color=self.HOVER_COLOR,
                    text_color=self.TEXT_COLOR, font=("Segoe UI", 12),
                    border_width=0, corner_radius=6
                )
                btn.grid(row=week, column=day, padx=1, pady=1, sticky="nsew")
                week_buttons.append(btn)
            self.day_buttons.append(week_buttons)

        # Configure grid weights
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def update_calendar(self):
        # Update month/year label
        month_name = calendar.month_name[self.display_date.month]
        self.month_year_label.configure(text=f"{month_name} {self.display_date.year}")

        # Get calendar data
        cal = calendar.monthcalendar(self.display_date.year, self.display_date.month)

        # Clear all buttons
        for week in self.day_buttons:
            for btn in week:
                btn.configure(text="", command=None, state="disabled")

        # Fill in days
        today = datetime.now().date()
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue

                btn = self.day_buttons[week_num][day_num]
                current_date = self.display_date.replace(day=day)

                btn.configure(
                    text=str(day),
                    command=lambda d=current_date: self.select_date(d),
                    state="normal"
                )

                # Styling based on date status
                if current_date == self.selected_date:
                    # Selected date
                    btn.configure(
                        fg_color=self.ACCENT_COLOR,
                        text_color="white",
                        hover_color="#2563eb"
                    )
                elif current_date == today:
                    # Today
                    btn.configure(
                        fg_color="transparent",
                        text_color=self.ACCENT_COLOR,
                        hover_color=self.HOVER_COLOR,
                        border_width=2,
                        border_color=self.ACCENT_COLOR
                    )
                elif current_date < today:
                    # Past dates
                    btn.configure(
                        fg_color="transparent",
                        text_color=self.SECONDARY_TEXT,
                        hover_color="#f3f4f6"
                    )
                else:
                    # Future dates
                    btn.configure(
                        fg_color="transparent",
                        text_color=self.TEXT_COLOR,
                        hover_color=self.HOVER_COLOR,
                        border_width=0
                    )

    def select_date(self, date):
        self.selected_date = date
        self.update_calendar()
        if self.callback:
            self.callback(date)

    def prev_month(self):
        if self.display_date.month == 1:
            self.display_date = self.display_date.replace(year=self.display_date.year - 1, month=12)
        else:
            self.display_date = self.display_date.replace(month=self.display_date.month - 1)
        self.update_calendar()

    def next_month(self):
        if self.display_date.month == 12:
            self.display_date = self.display_date.replace(year=self.display_date.year + 1, month=1)
        else:
            self.display_date = self.display_date.replace(month=self.display_date.month + 1)
        self.update_calendar()

    def get_date(self):
        return self.selected_date

    def set_date(self, date):
        self.selected_date = date
        self.display_date = date.replace(day=1)
        self.update_calendar()


class ModernDateEntry(ctk.CTkFrame):
    def __init__(self, parent, initial_date=None, date_format="%Y-%m-%d", **kwargs):
        super().__init__(parent, **kwargs)

        self.date_format = date_format
        self.selected_date = initial_date or datetime.now().date()
        self.popup = None

        # Styling
        self.configure(fg_color="transparent")

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Date display button
        self.date_button = ctk.CTkButton(
            self, text="", height=30, width=200,
            fg_color="white", hover_color="#f8fafc",
            text_color="#374151", font=("Segoe UI", 12),
            border_width=1, border_color="#d1d5db",
            corner_radius=6, anchor="w",
            command=self.show_calendar
        )
        self.date_button.pack(side="left", fill="x", expand=True)

        # Calendar icon
        calendar_btn = ctk.CTkButton(
            self, text="📅", width=30, height=30,
            fg_color="#3b82f6", hover_color="#2563eb",
            text_color="white", font=("Arial", 12),
            corner_radius=6, command=self.show_calendar
        )
        calendar_btn.pack(side="right", padx=(5, 0))

    def update_display(self):
        formatted_date = self.selected_date.strftime(self.date_format)
        self.date_button.configure(text=f"  {formatted_date}")

    def show_calendar(self):
        if self.popup:
            return

        # Create popup window
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Select Date")
        self.popup.geometry("320x380")
        self.popup.resizable(False, False)
        self.popup.grab_set()

        # Position popup near the date entry
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 5
        self.popup.geometry(f"+{x}+{y}")

        # Create date picker
        date_picker = ModernDatePicker(
            self.popup,
            initial_date=self.selected_date,
            callback=self.on_date_selected
        )
        date_picker.pack(fill="both", expand=True, padx=10, pady=10)

        # Close button
        close_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        close_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            close_frame, text="Close", width=80, height=30,
            fg_color="#6b7280", hover_color="#4b5563",
            command=self.close_calendar
        ).pack(side="right")

        # Handle popup close
        self.popup.protocol("WM_DELETE_WINDOW", self.close_calendar)

    def on_date_selected(self, date):
        self.selected_date = date
        self.update_display()
        self.close_calendar()

    def close_calendar(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None

    def get(self):
        """Return date as string in the specified format"""
        return self.selected_date.strftime(self.date_format)

    def get_date(self):
        """Return date as datetime.date object"""
        return self.selected_date

    def set_date(self, date):
        """Set the date (accepts datetime.date or string)"""
        if isinstance(date, str):
            self.selected_date = datetime.strptime(date, self.date_format).date()
        else:
            self.selected_date = date
        self.update_display()
