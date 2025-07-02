# ============== Imports ==============
from tkinter import messagebox
import customtkinter as ctk             # customtkinter

from models.auth import AuthModel
from utils.helpers import log
from utils.session import Session


# ============== Login Screen ==============
class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, dashboard_callback):
        super().__init__(parent)
        self.configure(fg_color="#f0f2f5")  # Light background

        self.callback = dashboard_callback  # function to call when login is successful
        self.auth_model = AuthModel()

        self.create_widgets()           # initializes UI components


    # ============== Widget Creation ==============
    def create_widgets(self):
        # Main container frame
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both")

        # Center the login card
        login_card = ctk.CTkFrame(main_container,
                                 width=450,
                                 height=600,
                                 corner_radius=20,
                                 fg_color="white",
                                 border_width=1,
                                 border_color="#e1e8ed")
        login_card.pack(expand=True, pady=50)
        login_card.pack_propagate(False)

        # Hotel icon/logo area
        logo_frame = ctk.CTkFrame(login_card,
                                 height=80,
                                 fg_color="transparent",
                                 corner_radius=15)
        logo_frame.pack(pady=(40, 30), padx=40, fill="x")

        # Hotel icon (using text for now, can be replaced with actual logo)
        hotel_icon = ctk.CTkLabel(logo_frame,
                                 text="🏨",
                                 font=("Arial", 32))
        hotel_icon.pack(pady=15)

        # ---- Title Label ----
        self.title_label = ctk.CTkLabel(login_card,
                                  text="Hotel Management System",
                                  font=("Segoe UI", 26, "bold"),
                                  text_color="#1f538d")
        self.title_label.pack(pady=(0, 10))

        # ---- Subtitle Label ----
        self.subtitle = ctk.CTkLabel(login_card,
                                     text="Sign in to your account",
                                     font=("Segoe UI", 14),
                                     text_color="#64748b")
        self.subtitle.pack(pady=(0, 40))

        # Form container
        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(pady=0, padx=40, fill="x")

        # Employee ID label and entry
        employee_label = ctk.CTkLabel(form_frame,
                                     text="Employee ID",
                                     font=("Segoe UI", 13, "bold"),
                                     text_color="#374151")
        employee_label.pack(anchor="w", pady=(0, 5))

        self.employee_id_entry = ctk.CTkEntry(form_frame,
                                             placeholder_text="Enter your employee ID",
                                             height=45,
                                             font=("Segoe UI", 13),
                                             corner_radius=8,
                                             border_width=2,
                                             border_color="#e5e7eb",
                                             fg_color="white")
        self.employee_id_entry.pack(fill="x", pady=(0, 20))
        self.employee_id_entry.bind('<Return>', lambda e: self.password_entry.focus_set())

        # Password label and entry
        password_label = ctk.CTkLabel(form_frame,
                                     text="Password",
                                     font=("Segoe UI", 13, "bold"),
                                     text_color="#374151")
        password_label.pack(anchor="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(form_frame,
                                          placeholder_text="Enter your password",
                                          show="*",
                                          height=45,
                                          font=("Segoe UI", 13),
                                          corner_radius=8,
                                          border_width=2,
                                          border_color="#e5e7eb",
                                          fg_color="white")
        self.password_entry.pack(fill="x", pady=(0, 15))
        self.password_entry.bind('<Return>', self.check_login)

        # ---- Forgot Password Button ----
        self.forget_password_button = ctk.CTkButton(form_frame,
                                                    text="Forgot Password?",
                                                    fg_color="transparent",
                                                    text_color="#1f538d",
                                                    hover_color="#f8fafc",
                                                    font=("Segoe UI", 12),
                                                    height=25,
                                                    command=self.forgot_password)
        self.forget_password_button.pack(anchor="e", pady=(0, 25))

        # ---- Login Button ----
        self.login_button = ctk.CTkButton(form_frame,
                                          text="Sign In",
                                          height=45,
                                          font=("Segoe UI", 14, "bold"),
                                          fg_color="#1f538d",
                                          hover_color="#1e40af",
                                          corner_radius=8,
                                          command=self.check_login)
        self.login_button.pack(fill="x", pady=(0, 30))

        # Footer
        footer_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20)

        footer_text = ctk.CTkLabel(footer_frame,
                                  text="© 2025 Hotel Management System",
                                  font=("Segoe UI", 11),
                                  text_color="#9ca3af")
        footer_text.pack()

        # Auto focus on employee ID entry after a short delay
        self.after(100, lambda: self.employee_id_entry.focus_set())


    # ============== Events ==============
    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Please contact your system administrator for password reset.")


    def check_login(self, event=None):
        employee_id = self.employee_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not employee_id or not password:
            messagebox.showwarning("Missing Fields", "Please enter both Employee ID and Password.")
            log(f"Login attempt failed: Empty employee_id or password.")
            return

        # Add loading state to button
        original_text = self.login_button.cget("text")
        self.login_button.configure(text="Signing In...", state="disabled")
        self.update()

        user = self.auth_model.login(employee_id=employee_id, password=password)
        print(f"User object returned: {user}")

        # Reset button state
        self.login_button.configure(text=original_text, state="normal")

        if user:
            Session.current_user = user
            print(f"Current User: {Session.current_user}")

            full_name = f"{user['FIRST_NAME']} {user['LAST_NAME']}"
            log(f"Login success: [{employee_id}] - {full_name}")

            self.employee_id_entry.unbind("<Return>")
            self.password_entry.unbind("<Return>")
            self.callback()  # Proceed to dashboard
        else:
            log(f"Login failed for employee id: [{employee_id}]")
            messagebox.showerror("Login Failed", "Invalid Employee ID or Password. Please try again.")
            # Clear password field on failed login
            self.password_entry.delete(0, 'end')
            self.employee_id_entry.focus_set()
