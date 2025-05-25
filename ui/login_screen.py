import customtkinter as ctk             # customtkinter
from models.user import User            # backend logic for authentication

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, dashboard_callback):
        super().__init__(master)
        self.callback = dashboard_callback  # function to call when login is successful

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=20)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=20)
        login_btn = ctk.CTkButton(self, text="Login", command=self.check_login)
        login_btn.pack(pady=20)
        self.error_label = ctk.CTkLabel(self, text="", text_color="dark red")
        self.error_label.pack()

    def set_login_success_callback(self, callback):
        self.callback = callback

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = User(username)
        if user.authenticate(password):
            self.callback()
        else:
            self.error_label.configure(text="Invalid credentials")
