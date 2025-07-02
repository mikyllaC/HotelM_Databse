import customtkinter as ctk
from tkinter import messagebox
import datetime

from models.employee import EmployeeModel
from utils.helpers import log
from ui.components.customDropdown import CustomDropdown


class EditStaffFrame(ctk.CTkFrame):
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
    BG_COLOR_2 = "white"

    def __init__(self, parent_popup, parent_page=None, employee_id=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.parent_page = parent_page
        self.employee_id = employee_id
        self.employee_model = EmployeeModel()

        self.entries = {}  # Store references to all entry widgets for later access
        self.create_widgets()

        if employee_id:
            self.load_employee_data(employee_id)

    # ============== Widget Creation ==============
    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self,
                                    fg_color="#F7F7F7",
                                    corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Edit Staff Member", font=("Roboto Condensed", 24), text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Employee ID ==========
        if self.employee_id:
            id_label = ctk.CTkLabel(self, text=f"Employee ID: {self.employee_id}", font=("Roboto Mono", 12, "bold"),
                                    text_color="#5c5c5c")
            id_label.pack()

        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(50, 20), fill="both", expand=True)

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

        # ========== Gender (Using CustomDropdown) ==========
        label = ctk.CTkLabel(form_frame, text="Gender *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=2, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.gender_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=2, column=1,
            options=["Male", "Female", "Other"],
            placeholder="Select Gender",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False,
            entry_name="entry_gender"
        )

        # ========== Contact Number ==========
        label = ctk.CTkLabel(form_frame, text="Phone *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=3, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="09123456789")
        entry.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_contact_number"] = entry

        # ========== Email ==========
        label = ctk.CTkLabel(form_frame, text="Email *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=4, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="email@email.com")
        entry.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_email"] = entry

        # ========== Date of Birth ==========
        label = ctk.CTkLabel(form_frame, text="Date of Birth *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=5, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="YYYY-MM-DD")
        entry.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_date_of_birth"] = entry

        # ========== Address ==========
        label = ctk.CTkLabel(form_frame, text="Address", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=6, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_address"] = entry

        # ========== Position (Using CustomDropdown) ==========
        label = ctk.CTkLabel(form_frame, text="Position *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=7, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.position_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=7, column=1,
            options=["Front Desk Clerk", "Housekeeper", "Maintenance", "Security", "Manager",
                    "Receptionist", "Concierge", "Chef", "Server", "Accountant", "Other"],
            placeholder="Select Position",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False,
            entry_name="entry_position"
        )

        # ========== Hire Date ==========
        label = ctk.CTkLabel(form_frame, text="Hire Date *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=8, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="YYYY-MM-DD")
        entry.grid(row=8, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_hire_date"] = entry

        # ========== Salary ==========
        label = ctk.CTkLabel(form_frame, text="Salary", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=9, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="0.00")
        entry.grid(row=9, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_salary"] = entry

        # ========== Assigned To ==========
        label = ctk.CTkLabel(form_frame, text="Assigned To", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=10, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        entry = ctk.CTkEntry(form_frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR,
                             placeholder_text="Floor, Department, etc.")
        entry.grid(row=10, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_assigned_to"] = entry

        # ========== Status (Using CustomDropdown) ==========
        label = ctk.CTkLabel(form_frame, text="Status *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=11, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.status_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=11, column=1,
            options=["Active", "Inactive", "On Leave"],
            placeholder="Select Status",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False,
            entry_name="entry_status"
        )

        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=12, column=1, pady=(50, 20), sticky="ew")

        # ========== Update Button ==========
        self.update_button = ctk.CTkButton(button_frame, text="Update", command=self.on_update,
                                           height=30, width=80)
        self.update_button.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # ========== Reset Button ==========
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_form,
                                          height=30, width=80, fg_color="#F7F7F7", text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.reset_button.grid(row=0, column=2, sticky="w")

    def load_employee_data(self, employee_id):
        employee = self.employee_model.get_employee_details(employee_id)
        if not employee:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Fill in fields
        self.entries["entry_first_name"].insert(0, employee["FIRST_NAME"])
        self.entries["entry_last_name"].insert(0, employee["LAST_NAME"])
        self.gender_dropdown.set(employee["GENDER"])
        self.entries["entry_contact_number"].insert(0, employee["CONTACT_NUMBER"])
        self.entries["entry_email"].insert(0, employee["EMAIL"])
        self.entries["entry_date_of_birth"].insert(0, employee["DATE_OF_BIRTH"])
        self.entries["entry_address"].insert(0, employee["ADDRESS"] or "")
        self.position_dropdown.set(employee["POSITION"])
        self.entries["entry_hire_date"].insert(0, employee["HIRE_DATE"])
        self.entries["entry_salary"].insert(0, str(employee["SALARY"]) if employee["SALARY"] else "")
        self.entries["entry_assigned_to"].insert(0, employee["ASSIGNED_TO"] or "")
        self.status_dropdown.set(employee["STATUS"])

    def on_update(self):
        if not self.validate_form():
            return

        # Collect data from entries and dropdowns
        employee_data = {
            "FIRST_NAME": self.entries["entry_first_name"].get().strip(),
            "LAST_NAME": self.entries["entry_last_name"].get().strip(),
            "GENDER": self.entries["entry_gender"].get(),
            "CONTACT_NUMBER": self.entries["entry_contact_number"].get().strip(),
            "EMAIL": self.entries["entry_email"].get().strip(),
            "DATE_OF_BIRTH": self.entries["entry_date_of_birth"].get().strip(),
            "ADDRESS": self.entries["entry_address"].get().strip(),
            "POSITION": self.entries["entry_position"].get(),
            "HIRE_DATE": self.entries["entry_hire_date"].get().strip(),
            "SALARY": float(self.entries["entry_salary"].get().strip()) if self.entries["entry_salary"].get().strip() else 0.0,
            "ASSIGNED_TO": self.entries["entry_assigned_to"].get().strip(),
            "STATUS": self.entries["entry_status"].get()
        }

        try:
            self.employee_model.update_employee_details(self.employee_id, employee_data)
            messagebox.showinfo("Success", "Staff member updated successfully!")
            if self.parent_page:
                self.parent_page.populate_employee_data()
            self.master.destroy()
        except Exception as e:
            log(f"Error updating staff member: {str(e)}")
            messagebox.showerror("Error", f"Failed to update staff member: {e}")

    def validate_form(self):
        required_fields = [
            ("entry_first_name", "First Name"),
            ("entry_last_name", "Last Name"),
            ("entry_gender", "Gender"),
            ("entry_contact_number", "Contact Number"),
            ("entry_email", "Email"),
            ("entry_date_of_birth", "Date of Birth"),
            ("entry_position", "Position"),
            ("entry_hire_date", "Hire Date"),
            ("entry_status", "Status")
        ]

        for field_key, field_name in required_fields:
            if not self.entries[field_key].get().strip():
                messagebox.showerror("Missing Required Field", f"{field_name} is required.")
                log(f"{field_name} is required.")
                return False

        # Validate date formats
        try:
            datetime.datetime.strptime(self.entries["entry_date_of_birth"].get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date of Birth must be in YYYY-MM-DD format.")
            return False

        try:
            datetime.datetime.strptime(self.entries["entry_hire_date"].get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Hire Date must be in YYYY-MM-DD format.")
            return False

        # Validate salary if provided
        if self.entries["entry_salary"].get().strip():
            try:
                salary = float(self.entries["entry_salary"].get().strip())
                if salary < 0:
                    messagebox.showerror("Invalid Salary", "Salary cannot be negative.")
                    return False
            except ValueError:
                messagebox.showerror("Invalid Salary", "Salary must be a valid number.")
                return False

        return True

    def reset_form(self):
        # Clear all entry fields and reload original data
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, 'end')

        # Reload the original employee data
        if self.employee_id:
            self.load_employee_data(self.employee_id)
