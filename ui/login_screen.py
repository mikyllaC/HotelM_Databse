import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.callback = None

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=20)

        login_btn = ctk.CTkButton(self, text="Login", command=self.check_login)
        login_btn.pack(pady=20)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    def set_login_success_callback(self, callback):
        self.callback = callback

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # TODO: Replace this with your actual authentication logic from models/user.py
        if username == "admin" and password == "password":
            if self.callback:
                self.callback()
        else:
            self.error_label.configure(text="Invalid credentials!")