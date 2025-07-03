# ============== Imports ==============
from tkinter import messagebox
import customtkinter as ctk
import datetime

from models.auth import AuthModel
from utils.helpers import log


# ============== Signup Screen ==============
class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.configure(fg_color="#f0f2f5")  # Light background

        self.login_callback = login_callback  # function to call to return to login
        self.auth_model = AuthModel()

        self.create_widgets()           # initializes UI components


    # ============== Widget Creation ==============
    def create_widgets(self):
        # Main container frame with scrolling
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Center the signup card
        signup_card = ctk.CTkFrame(self.main_container,
                                 width=500,
                                 height=1000,
                                 corner_radius=20,
                                 fg_color="white",
                                 border_width=1,
                                 border_color="#e1e8ed")
        signup_card.pack(expand=True, pady=20)
        signup_card.pack_propagate(False)

        # Hotel icon/logo area
        logo_frame = ctk.CTkFrame(signup_card,
                                 height=60,  # Reduced height
                                 fg_color="transparent",
                                 corner_radius=15)
        logo_frame.pack(pady=(20, 15), padx=40, fill="x")

        # Hotel icon
        hotel_icon = ctk.CTkLabel(logo_frame,
                                 text="🏨",
                                 font=("Arial", 28))  # Slightly smaller
        hotel_icon.pack(pady=5)

        # ---- Title Label ----
        self.title_label = ctk.CTkLabel(signup_card,
                                  text="Hotel Management System",
                                  font=("Segoe UI", 22, "bold"),  # Slightly smaller
                                  text_color="#1f538d")
        self.title_label.pack(pady=(0, 5))

        # ---- Subtitle Label ----
        self.subtitle = ctk.CTkLabel(signup_card,
                                     text="Create new employee account",
                                     font=("Segoe UI", 13),  # Slightly smaller
                                     text_color="#64748b")
        self.subtitle.pack(pady=(0, 20))

        # Form container
        form_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        form_frame.pack(pady=0, padx=30, fill="both", expand=True)  # Added expand=True

        # Personal Information Section
        personal_section = ctk.CTkLabel(form_frame,
                                       text="Personal Information",
                                       font=("Segoe UI", 14, "bold"),  # Slightly smaller
                                       text_color="#1f538d")
        personal_section.pack(anchor="w", pady=(0, 10))

        # First Name and Last Name (side by side)
        name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))

        # First Name
        fname_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        fname_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

        fname_label = ctk.CTkLabel(fname_frame,
                                  text="First Name *",
                                  font=("Segoe UI", 13, "bold"),
                                  text_color="#374151")
        fname_label.pack(anchor="w", pady=(0, 5))

        self.first_name_entry = ctk.CTkEntry(fname_frame,
                                            placeholder_text="Enter first name",
                                            height=40,
                                            font=("Segoe UI", 13),
                                            corner_radius=8,
                                            border_width=2,
                                            border_color="#e5e7eb",
                                            fg_color="white")
        self.first_name_entry.pack(fill="x")

        # Last Name
        lname_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        lname_frame.pack(side="left", expand=True, fill="x", padx=(10, 0))

        lname_label = ctk.CTkLabel(lname_frame,
                                  text="Last Name *",
                                  font=("Segoe UI", 13, "bold"),
                                  text_color="#374151")
        lname_label.pack(anchor="w", pady=(0, 5))

        self.last_name_entry = ctk.CTkEntry(lname_frame,
                                           placeholder_text="Enter last name",
                                           height=40,
                                           font=("Segoe UI", 13),
                                           corner_radius=8,
                                           border_width=2,
                                           border_color="#e5e7eb",
                                           fg_color="white")
        self.last_name_entry.pack(fill="x")

        # Gender and Date of Birth (side by side)
        gender_dob_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_dob_frame.pack(fill="x", pady=(0, 15))

        # Gender
        gender_frame = ctk.CTkFrame(gender_dob_frame, fg_color="transparent")
        gender_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

        gender_label = ctk.CTkLabel(gender_frame,
                                   text="Gender *",
                                   font=("Segoe UI", 13, "bold"),
                                   text_color="#374151")
        gender_label.pack(anchor="w", pady=(0, 5))

        self.gender_dropdown = ctk.CTkComboBox(gender_frame,
                                              values=["Male", "Female", "Other"],
                                              height=40,
                                              font=("Segoe UI", 13),
                                              corner_radius=8,
                                              border_width=2,
                                              border_color="#e5e7eb",
                                              fg_color="white")
        self.gender_dropdown.pack(fill="x")
        self.gender_dropdown.set("Select Gender")

        # Date of Birth
        dob_frame = ctk.CTkFrame(gender_dob_frame, fg_color="transparent")
        dob_frame.pack(side="left", expand=True, fill="x", padx=(10, 0))

        dob_label = ctk.CTkLabel(dob_frame,
                                text="Date of Birth *",
                                font=("Segoe UI", 13, "bold"),
                                text_color="#374151")
        dob_label.pack(anchor="w", pady=(0, 5))

        self.dob_entry = ctk.CTkEntry(dob_frame,
                                     placeholder_text="YYYY-MM-DD",
                                     height=40,
                                     font=("Segoe UI", 13),
                                     corner_radius=8,
                                     border_width=2,
                                     border_color="#e5e7eb",
                                     fg_color="white")
        self.dob_entry.pack(fill="x")

        # Contact Information
        contact_label = ctk.CTkLabel(form_frame,
                                    text="Contact Number *",
                                    font=("Segoe UI", 13, "bold"),
                                    text_color="#374151")
        contact_label.pack(anchor="w", pady=(0, 5))

        self.contact_entry = ctk.CTkEntry(form_frame,
                                         placeholder_text="Enter contact number",
                                         height=40,
                                         font=("Segoe UI", 13),
                                         corner_radius=8,
                                         border_width=2,
                                         border_color="#e5e7eb",
                                         fg_color="white")
        self.contact_entry.pack(fill="x", pady=(0, 15))

        # Email
        email_label = ctk.CTkLabel(form_frame,
                                  text="Email Address *",
                                  font=("Segoe UI", 13, "bold"),
                                  text_color="#374151")
        email_label.pack(anchor="w", pady=(0, 5))

        self.email_entry = ctk.CTkEntry(form_frame,
                                       placeholder_text="Enter email address",
                                       height=40,
                                       font=("Segoe UI", 13),
                                       corner_radius=8,
                                       border_width=2,
                                       border_color="#e5e7eb",
                                       fg_color="white")
        self.email_entry.pack(fill="x", pady=(0, 15))

        # Position
        position_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        position_frame.pack(fill="x", pady=(0, 15))

        # Position
        position_frame = ctk.CTkFrame(position_frame, fg_color="transparent")
        position_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

        position_label = ctk.CTkLabel(position_frame,
                                     text="Position *",
                                     font=("Segoe UI", 13, "bold"),
                                     text_color="#374151")
        position_label.pack(anchor="w", pady=(0, 5))

        self.position_dropdown = ctk.CTkComboBox(position_frame,
                                                values=["Front Desk", "Housekeeping", "Manager", "Maintenance", "Security", "Chef", "Waiter", "Receptionist"],
                                                height=40,
                                                font=("Segoe UI", 13),
                                                corner_radius=8,
                                                border_width=2,
                                                border_color="#e5e7eb",
                                                fg_color="white")
        self.position_dropdown.pack(fill="x")
        self.position_dropdown.set("Select Position")

        # Authentication Section
        auth_section = ctk.CTkLabel(form_frame,
                                   text="Authentication",
                                   font=("Segoe UI", 16, "bold"),
                                   text_color="#1f538d")
        auth_section.pack(anchor="w", pady=(0, 15))

        # Password and Confirm Password (side by side)
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))

        # Password
        pass_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        pass_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))

        password_label = ctk.CTkLabel(pass_frame,
                                     text="Password",
                                     font=("Segoe UI", 13, "bold"),
                                     text_color="#374151")
        password_label.pack(anchor="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(pass_frame,
                                          placeholder_text="Enter password (optional)",
                                          show="*",
                                          height=40,
                                          font=("Segoe UI", 13),
                                          corner_radius=8,
                                          border_width=2,
                                          border_color="#e5e7eb",
                                          fg_color="white")
        self.password_entry.pack(fill="x")

        # Confirm Password
        confirm_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        confirm_frame.pack(side="left", expand=True, fill="x", padx=(10, 0))

        confirm_label = ctk.CTkLabel(confirm_frame,
                                    text="Confirm Password",
                                    font=("Segoe UI", 13, "bold"),
                                    text_color="#374151")
        confirm_label.pack(anchor="w", pady=(0, 5))

        self.confirm_password_entry = ctk.CTkEntry(confirm_frame,
                                                  placeholder_text="Confirm password",
                                                  show="*",
                                                  height=40,
                                                  font=("Segoe UI", 13),
                                                  corner_radius=8,
                                                  border_width=2,
                                                  border_color="#e5e7eb",
                                                  fg_color="white")
        self.confirm_password_entry.pack(fill="x")

        # Password info
        password_info = ctk.CTkLabel(form_frame,
                                    text="Leave password blank to auto-generate one",
                                    font=("Segoe UI", 11),
                                    text_color="#9ca3af")
        password_info.pack(anchor="w", pady=(5, 20))

        # ---- Signup Button ----
        self.signup_button = ctk.CTkButton(form_frame,
                                          text="Create Account",
                                          height=45,
                                          font=("Segoe UI", 14, "bold"),
                                          fg_color="#1f538d",
                                          hover_color="#1e40af",
                                          corner_radius=8,
                                          command=self.handle_signup)
        self.signup_button.pack(fill="x", pady=(0, 15))

        # ---- Back to Login Button ----
        self.back_button = ctk.CTkButton(form_frame,
                                        text="Back to Login",
                                        fg_color="transparent",
                                        text_color="#1f538d",
                                        hover_color="#f8fafc",
                                        font=("Segoe UI", 12),
                                        height=35,
                                        command=self.back_to_login)
        self.back_button.pack(fill="x", pady=(0, 20))

        # Footer
        footer_frame = ctk.CTkFrame(signup_card, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20)

        footer_text = ctk.CTkLabel(footer_frame,
                                  text="© 2025 Hotel Management System",
                                  font=("Segoe UI", 11),
                                  text_color="#9ca3af")
        footer_text.pack()


    # ============== Events ==============
    def validate_form(self):
        """Validate all required form fields"""
        errors = []

        # Required fields validation
        if not self.first_name_entry.get().strip():
            errors.append("First Name is required")
        if not self.last_name_entry.get().strip():
            errors.append("Last Name is required")
        if self.gender_dropdown.get() == "Select Gender":
            errors.append("Gender is required")
        if not self.dob_entry.get().strip():
            errors.append("Date of Birth is required")
        if not self.contact_entry.get().strip():
            errors.append("Contact Number is required")
        if not self.email_entry.get().strip():
            errors.append("Email is required")
        if self.position_dropdown.get() == "Select Position":
            errors.append("Position is required")

        # Date format validation
        try:
            if self.dob_entry.get().strip():
                datetime.datetime.strptime(self.dob_entry.get().strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("Date of Birth must be in YYYY-MM-DD format")

        # Email format validation (basic)
        email = self.email_entry.get().strip()
        if email and "@" not in email:
            errors.append("Invalid email format")

        # Password validation
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if password and password != confirm_password:
            errors.append("Passwords do not match")

        if password and len(password) < 6:
            errors.append("Password must be at least 6 characters long")

        return errors

    def handle_signup(self):
        """Handle the signup process"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Prepare employee data
        employee_data = {
            "FIRST_NAME": self.first_name_entry.get().strip(),
            "LAST_NAME": self.last_name_entry.get().strip(),
            "GENDER": self.gender_dropdown.get(),
            "CONTACT_NUMBER": self.contact_entry.get().strip(),
            "EMAIL": self.email_entry.get().strip(),
            "DATE_OF_BIRTH": self.dob_entry.get().strip(),
            "ADDRESS": "Not provided",  # Default value since field was removed
            "POSITION": self.position_dropdown.get(),
            "HIRE_DATE": datetime.date.today().isoformat(),
            "SALARY": 0.0,  # Default value since field was removed
            "ASSIGNED_TO": "Unassigned",  # Default value since field was removed
            "STATUS": "Available"
        }

        password = self.password_entry.get().strip() if self.password_entry.get().strip() else None

        try:
            # Attempt to register the employee
            success, message, employee_id = self.auth_model.signup(employee_data, password)

            if success:
                messagebox.showinfo("Registration Successful", message)
                self.back_to_login()
            else:
                messagebox.showerror("Registration Failed", message)

        except Exception as e:
            log(f"Signup error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during registration: {str(e)}")

    def back_to_login(self):
        """Return to the login screen"""
        self.login_callback()
