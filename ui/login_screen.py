# ============== Imports ==============
import tkinter as tk                    # tkinter
import customtkinter as ctk             # customtkinter
from models.user import User            # backend logic for authentication


# ============== Login Screen ==============
class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, dashboard_callback):
        super().__init__(master)

        self.callback = dashboard_callback  # function to call when login is successful
        self.create_widgets()           # initializes UI components


    # ============== Widget Creation ==============
    def create_widgets(self):
        # ---- Title Label ----
        self.label = ctk.CTkLabel(self,
            text="Hotel Management System", font=("Arial", 24, "bold"), text_color="black", justify="center",
            width=50,height=100)
        self.label.pack(pady=(1, 10), padx=10)

        # ---- Subtitle Label ----
        self.subtitle = ctk.CTkLabel(self,
            text="Please log in to continue",font=("Arial", 16),text_color="gray",justify="center")
        self.subtitle.pack(pady=(2, 30), padx=5)

        # ---- Entry Fields ----
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Employee ID")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        # ---- Forgot Password Button ----
        self.forget_password_button = ctk.CTkButton(self,
            text="Forgot Password?", fg_color="transparent", text_color="blue", hover_color="#FFFFFF",
            command=self.forgot_password)
        self.forget_password_button.pack(pady=10)

        # ---- Login Button ----
        self.login_button = ctk.CTkButton(self, text="Log In", width=150, command=self.check_login)
        self.login_button.pack(pady=20, padx=20,)


    # ============== Events ==============
    def forgot_password(self):
        # Triggered when 'Forgot Password?' is clicked.
        tk.messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")


    def check_login(self):
        # Checks user credentials and proceeds if authentication succeeds
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = User(username)
        if user.authenticate(password):
            self.callback()             # runs the on_login_success function (from main.py) inside callback
        else:
            tk.messagebox.showerror("Login Failed", "Invalid credentials.")