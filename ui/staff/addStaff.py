import customtkinter as ctk
import datetime
from tkinter import messagebox

from models.employee import EmployeeModel


class AddStaffFrame(ctk.CTkFrame):
    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")    # Set background color of the frame
        self.parent_page = parent_page
        self.employee_model = EmployeeModel()
        self.create_widgets()


    # ============== Widget Creation ==============
    def create_widgets(self):
        # ========== Header ==========
        header = ctk.CTkLabel(self, text="Add New Staff", font=("Arial", 24, "bold"), text_color="black")
        header.pack(pady=(30, 20))

        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="#f4f4f4")     # Light gray form container
        form_frame.pack(padx=40, pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure((0, 1), weight=1) # Make both columns expand equally

        self.entries = {} # Store references to all entry widgets for later access

        # ========== First Name ==========
        label = ctk.CTkLabel(form_frame, text="First Name:", font=("Arial", 14), text_color="black")
        label.grid(row=0, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35)
        entry.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_first_name"] = entry

        # ========== Last Name ==========
        label = ctk.CTkLabel(form_frame, text="Last Name:", font=("Arial", 14), text_color="black")
        label.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35)
        entry.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_last_name"] = entry

        # ========== Gender (Dropdown) ==========
        label = ctk.CTkLabel(form_frame, text="Gender:", font=("Arial", 14), text_color="black")
        label.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)
        gender_dropdown = ctk.CTkOptionMenu(form_frame, values=["Male", "Female", "Other"])
        gender_dropdown.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_gender"] = gender_dropdown

        # ========== Contact Number ==========
        label = ctk.CTkLabel(form_frame, text="Contact Number:", font=("Arial", 14), text_color="black")
        label.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35)
        entry.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_phone"] = entry

        # ========== Email ==========
        label = ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 14), text_color="black")
        label.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35)
        entry.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_email"] = entry

        # ========== Date of Birth (Optional) ==========
        label = ctk.CTkLabel(form_frame, text="Date of Birth (Optional, YYYY-MM-DD):", font=("Arial", 14), text_color="black")
        label.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35, placeholder_text="YYYY-MM-DD")
        entry.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_date_of_birth"] = entry

        # ========== Address (Optional) ==========
        label = ctk.CTkLabel(form_frame, text="Address (Optional):", font=("Arial", 14), text_color="black")
        label.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35, placeholder_text="e.g. 123 Main Street")
        entry.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_address"] = entry

        # ========== Role (Dropdown) ==========
        label = ctk.CTkLabel(form_frame, text="Role:", font=("Arial", 14), text_color="black")
        label.grid(row=7, column=0, sticky="e", padx=(20, 10), pady=10)
        role_dropdown = ctk.CTkOptionMenu(form_frame, values=["Manager", "Receptionist", "Cleaner", "Security", "Chef"])
        role_dropdown.grid(row=7, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_role"] = role_dropdown

        # ========== Date Hired ==========
        label = ctk.CTkLabel(form_frame, text="Date Hired (YYYY-MM-DD):", font=("Arial", 14), text_color="black")
        label.grid(row=8, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35, placeholder_text="YYYY-MM-DD")
        entry.grid(row=8, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_hire_date"] = entry

        # ========== Salary ==========
        label = ctk.CTkLabel(form_frame, text="Salary:", font=("Arial", 14), text_color="black")
        label.grid(row=9, column=0, sticky="e", padx=(20, 10), pady=10)
        entry = ctk.CTkEntry(form_frame, width=300, height=35)
        entry.grid(row=9, column=1, sticky="w", padx=(0, 20), pady=10)
        self.entries["entry_salary"] = entry


        # ========== Buttons ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 30))

        # Save button — triggers save_staff method
        ctk.CTkButton(button_frame, text="Save", width=140,
                      command=self.save_staff).pack(side="left", padx=20)
        # Cancel button — closes the window
        ctk.CTkButton(button_frame, text="Cancel", width=140, fg_color="gray",
                      command=self.master.destroy).pack(side="left", padx=20)


    def save_staff(self):
        # Explicitly get each field's value
        first_name = self.entries["entry_first_name"].get().strip()
        last_name = self.entries["entry_last_name"].get().strip()
        gender = self.entries["entry_gender"].get()
        phone = self.entries["entry_phone"].get().strip()
        email = self.entries["entry_email"].get().strip()
        date_of_birth = self.entries["entry_date_of_birth"].get().strip()
        address = self.entries["entry_address"].get().strip()
        role = self.entries["entry_role"].get()
        hire_date = self.entries["entry_hire_date"].get().strip()
        salary = self.entries["entry_salary"].get().strip()

        # ========== Validations ==========
        if not first_name:
            messagebox.showerror("Missing Required Field", "First Name is required.")
            return
        if not last_name:
            messagebox.showerror("Missing Required Field", "Last Name is required.")
            return
        if not phone:
            messagebox.showerror("Missing Required Field", "Contact Number is required.")
            return

        if hire_date:
            try:
                datetime.datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date",
                                     "Please enter a valid Hire Date in YYYY-MM-DD format.")
                return
        else:
            hire_date = datetime.date.today().isoformat() # Default to today's date

        if date_of_birth:
            try:
                datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date",
                                     "Please enter a valid Date of Birth in YYYY-MM-DD format.")
                return
        else:
            date_of_birth = "Not Provided"

        staff_data = {
            "FIRST_NAME": first_name,
            "LAST_NAME": last_name,
            "GENDER": gender,
            "CONTACT_NUMBER": phone,
            "EMAIL": email,
            "DATE_OF_BIRTH": date_of_birth or "Not Provided",
            "ADDRESS": address or "Not Provided",
            "POSITION": role,
            "HIRE_DATE": hire_date,
            "SALARY": salary or "Not Provided",
            "STATUS": 'Active'
        }

        self.employee_model.add_employee(employee_data=staff_data)
        if self.parent_page:
            self.parent_page.populate_staff_list()  # refreshes tree after update
        self.master.destroy()