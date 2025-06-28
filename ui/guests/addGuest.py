import customtkinter as ctk
from tkinter import messagebox

from models.guest import GuestModel
from utils.helpers import log
from utils.session import Session


class AddGuestFrame(ctk.CTkFrame):
    FONT_LABEL = ("Roboto", 14)
    FONT_ENTRY = ("Roboto", 10)
    FONT_ENTRY_LABEL = ("Roboto", 12)
    TEXT_COLOR_LABEL = "black"
    TEXT_COLOR_ENTRY = "#818197"
    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    PADX_LABEL = (20, 80)


    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.parent_page = parent_page
        self.guest_model = GuestModel()

        self.entries = {}  # Store references to all entry widgets for later access
        self.create_widgets()

    # ============== Widget Creation ==============
    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self,
                                    fg_color="#F7F7F7",
                                    corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Add Guest", font=("Roboto Condensed", 24), text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.pack(fill="x", side="bottom")


        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(50,20), fill="both", expand=True)

        # ========== Name ==========
        name_label = ctk.CTkLabel(form_frame, text="Name *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        name_label.grid(row=0, column=0, sticky="nw", padx=self.PADX_LABEL)

        entry_name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        entry_name_frame.grid(row=0, column=1, pady=(0, 10), sticky="ew")

        entry_first_name = ctk.CTkEntry(entry_name_frame, width=150, height=self.ENTRY_HEIGHT, border_width=self.BORDER_WIDTH,
                                        border_color=self.BORDER_COLOR)
        entry_first_name.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entries["entry_first_name"] = entry_first_name

        entry_last_name = ctk.CTkEntry(entry_name_frame, width=150, height=self.ENTRY_HEIGHT, border_width=self.BORDER_WIDTH,
                                       border_color=self.BORDER_COLOR)
        entry_last_name.grid(row=0, column=1, sticky="w")
        self.entries["entry_last_name"] = entry_last_name

        label_first_name = ctk.CTkLabel(entry_name_frame, text="First Name", font=self.FONT_ENTRY_LABEL,
                                        text_color=self.TEXT_COLOR_ENTRY)
        label_first_name.grid(row=1, column=0, sticky="nw")
        label_last_name = ctk.CTkLabel(entry_name_frame, text="Last Name", font=self.FONT_ENTRY_LABEL,
                                       text_color=self.TEXT_COLOR_ENTRY)
        label_last_name.grid(row=1, column=1, sticky="nw")

        # ========== Contact Number ==========
        label = ctk.CTkLabel(form_frame, text="Phone *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=2, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="09123456789")
        entry.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_contact_number"] = entry

        # ========== Email ==========
        label = ctk.CTkLabel(form_frame, text="Email *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=3, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="email@email.com")
        entry.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_email"] = entry

        # ========== Address ==========
        address_label = ctk.CTkLabel(form_frame, text="Address", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        address_label.grid(row=4, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        # Frame for Address Entry Frames
        address_entry_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        address_entry_frame.grid(row=4, column=1, pady=(0, 10), sticky="ew")

        # Frame for Address Line 1
        address_l1_frame = ctk.CTkFrame(address_entry_frame, fg_color="transparent")
        address_l1_frame.grid(row=1, column=0, pady=(10, 0), sticky="ew")

        # Address Line 1
        entry_address_l1 = ctk.CTkEntry(address_l1_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                                        border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_address_l1.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.entries["entry_address_l1"] = entry_address_l1
        label_address_l1 = ctk.CTkLabel(address_l1_frame, text="Address Line 1", font=self.FONT_ENTRY_LABEL,
                                        text_color=self.TEXT_COLOR_ENTRY)
        label_address_l1.grid(row=1, column=0, sticky="nw")

        # Frame for Address Line 2
        address_l2_frame = ctk.CTkFrame(address_entry_frame, fg_color="transparent")
        address_l2_frame.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        # Address Line 2
        entry_address_l2 = ctk.CTkEntry(address_l2_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                                        border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_address_l2.grid(row=2, column=0, sticky="w", padx=(0, 20))
        self.entries["entry_address_l2"] = entry_address_l2
        label_address_l2 = ctk.CTkLabel(address_l2_frame, text="Address Line 2", font=self.FONT_ENTRY_LABEL,
                                        text_color=self.TEXT_COLOR_ENTRY)
        label_address_l2.grid(row=3, column=0, sticky="nw")

        # Frame for City and State
        city_state_frame = ctk.CTkFrame(address_entry_frame, fg_color="transparent")
        city_state_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # City
        entry_city = ctk.CTkEntry(city_state_frame, width=120, height=self.ENTRY_HEIGHT,
                                  border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_city.grid(row=4, column=0, sticky="w", padx=(0,10))
        self.entries["entry_city"] = entry_city
        label_city = ctk.CTkLabel(city_state_frame, text="City / State", font=self.FONT_ENTRY_LABEL,
                                  text_color=self.TEXT_COLOR_ENTRY)
        label_city.grid(row=5, column=0, sticky="nw")

        # State
        entry_state = ctk.CTkEntry(city_state_frame, width=120, height=self.ENTRY_HEIGHT,
                                   border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_state.grid(row=4, column=1, sticky="w")
        self.entries["entry_state"] = entry_state
        label_state = ctk.CTkLabel(city_state_frame, text="State / Province", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_state.grid(row=5, column=1, sticky="nw")

        # Frame for Postal and Country
        postal_country_frame = ctk.CTkFrame(address_entry_frame, fg_color="transparent")
        postal_country_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Postal
        entry_postal = ctk.CTkEntry(postal_country_frame, width=120, height=self.ENTRY_HEIGHT,
                                    border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_postal.grid(row=6, column=0, sticky="w", padx=(0,10))
        self.entries["entry_postal"] = entry_postal
        label_postal = ctk.CTkLabel(postal_country_frame, text="Postal Code", font=self.FONT_ENTRY_LABEL,
                                    text_color=self.TEXT_COLOR_ENTRY)
        label_postal.grid(row=7, column=0, sticky="nw")

        # Country
        entry_country = ctk.CTkEntry(postal_country_frame, width=120, height=self.ENTRY_HEIGHT,
                                     border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry_country.grid(row=6, column=1, sticky="w")
        self.entries["entry_country"] = entry_country
        label_country = ctk.CTkLabel(postal_country_frame, text="Country", font=self.FONT_ENTRY_LABEL,
                                     text_color=self.TEXT_COLOR_ENTRY)
        label_country.grid(row=7, column=1, sticky="nw")

        #self.entries["entry_address"] = entry_address

        # ========== Status ==========
        label = ctk.CTkLabel(form_frame, text="Status *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=5, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        status_dropdown = ctk.CTkOptionMenu(form_frame, values=["Checked Out", "Checked In", "In Transit"])
        status_dropdown.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_status"] = status_dropdown


        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=6, column=1, pady=(50, 20), sticky="ew")

        # ========== Submit Button ==========
        self.submit_button = ctk.CTkButton(button_frame, text="Add", command=self.on_submit,
                                           height=30, width=80)
        self.submit_button.grid(row=6, column=1, padx=(0,10), sticky="w")

        # ========== Rest Button ==========
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_form,
                                          height=30, width=80, fg_color="#F7F7F7", text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.reset_button.grid(row=6, column=2, sticky="w")


    def on_submit(self):
        if not self.validate_form():
            return

        employee_id = Session.current_user['EMPLOYEE_ID'] if Session.current_user else ''

        # Collect data from entries and dropdowns
        guest_data = {
            "FIRST_NAME": self.entries["entry_first_name"].get().strip(),
            "LAST_NAME": self.entries["entry_last_name"].get().strip(),
            "CONTACT_NUMBER": self.entries["entry_contact_number"].get().strip(),
            "EMAIL": self.entries["entry_email"].get().strip(),
            "ADDRESS_LINE1": self.entries["entry_address_l1"].get().strip(),
            "ADDRESS_LINE2": self.entries["entry_address_l2"].get().strip(),
            "CITY": self.entries["entry_city"].get().strip(),
            "STATE": self.entries["entry_state"].get().strip(),
            "POSTAL_CODE": self.entries["entry_postal"].get().strip(),
            "COUNTRY": self.entries["entry_country"].get().strip(),
            "STATUS": self.entries["entry_status"].get(),
            "EMPLOYEE_ID": employee_id
        }

        try:
            self.guest_model.add_guest(guest_data)
            messagebox.showinfo("Success", "Guest added successfully!")
            if self.parent_page:
                self.parent_page.populate_guest_data()
            self.master.destroy()
        except Exception as e:
            log(f"Error adding guest: {str(e)}")
            messagebox.showerror("Error", f"Failed to add guest: {e}")


    def validate_form(self):
        if not self.entries["entry_first_name"].get().strip():
            messagebox.showerror("Missing Required Field", "First Name is required.")
            log("First Name is required.")
            return False
        if not self.entries["entry_contact_number"].get().strip():
            messagebox.showerror("Missing Required Field", "Last Name is required.")
            log("Contact Number is required.")
            return False
        if not self.entries["entry_contact_number"].get().strip():
            messagebox.showerror("Missing Required Field", "Contact Number is required.")
            log("Contact Number is required.")
            return False
        if not self.entries["entry_email"].get().strip():
            messagebox.showerror("Missing Required Field", "Email Address is required.")
            log("Email Address is required.")
            return False
        return True


    def reset_form(self):
        # Clear all entry fields and reset dropdown
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, 'end')
        self.entries["entry_status"].set("Checked Out")  # Resetting to default value


