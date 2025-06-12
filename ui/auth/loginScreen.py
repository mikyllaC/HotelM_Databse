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

        self.callback = dashboard_callback  # function to call when login is successful
        self.auth_model = AuthModel()

        self.create_widgets()           # initializes UI components


    # ============== Widget Creation ==============
    def create_widgets(self):
        # ---- Title Label ----
        self.title_label = ctk.CTkLabel(self,
                                  text="Hotel Management System",
                                  font=("Arial", 24, "bold"),
                                  text_color="black",
                                  justify="center",
                                  width=50,
                                  height=100 )
        self.title_label.pack(pady=(50, 10), padx=10)

        # ---- Subtitle Label ----
        self.subtitle = ctk.CTkLabel(self,
                                     text="Please log in to continue",
                                     font=("Arial", 16),
                                     text_color="gray",
                                     justify="center" )
        self.subtitle.pack(pady=(2, 30), padx=5)

        # ---- Entry Fields ----
        self.employee_id_entry = ctk.CTkEntry(self, placeholder_text="Employee ID")
        self.employee_id_entry.pack(pady=10)
        self.employee_id_entry.bind('<Return>', lambda e: self.password_entry.focus_set())
        #self.after(100, lambda: self.employee_id_entry.focus_set()) # auto focus this entry

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', self.check_login)


        # ---- Forgot Password Button ----
        self.forget_password_button = ctk.CTkButton(self,
                                                    text="Forgot Password?",
                                                    fg_color="transparent",
                                                    text_color="blue",
                                                    hover_color="#FFFFFF",
                                                    command=self.forgot_password )
        self.forget_password_button.pack(pady=10)

        # ---- Login Button ----
        self.login_button = ctk.CTkButton(self,
                                          text="Log In",
                                          width=150,
                                          command=self.check_login )
        self.login_button.pack(pady=20, padx=20,)


    # ============== Events ==============
    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")


    def check_login(self, event=None):
        employee_id = self.employee_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not employee_id or not password:
            messagebox.showwarning("Missing Fields", "Please enter both Employee ID and Password.")
            log(f"Login attempt failed: Empty employee_id or password.")
            return

        user = self.auth_model.login(employee_id=employee_id, password=password)
        print(f"User object returned: {user}")

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
            messagebox.showerror("Login Failed", "Invalid credentials.")