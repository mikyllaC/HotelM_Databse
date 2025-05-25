import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue") 

class LogInPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(
            self,
            text="Hotel Management System",
            font=("Arial", 24, "bold"),
            text_color="black",
            justify="center",
            width=50,
            height=100
        )
        self.label.pack(pady=(1, 10), padx=10)

        self.subtitle = ctk.CTkLabel(
            self,
            text="Please log in to continue",
            font=("Arial", 16),
            text_color="gray",
            justify="center",
        )
        self.subtitle.pack(pady=(2, 30), padx=5)

        self.username_entry = ctk.CTkEntry(self, 
                                           placeholder_text="Employee ID")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.forget_password_button = ctk.CTkButton(
            self, 
            text="Forgot Password?", 
            fg_color="transparent", 
            text_color="blue", 
            hover_color="#FFFFFF",
    
            command=self.forget_password
          
        )
        self.forget_password_button.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Log In", width= 150, command=self.log_in)
        self.login_button.pack(
            pady=20,
            padx=20,
            )

    def forget_password(self):
        tk.messagebox.showinfo("Forgot Password", "Password reset instructions will be sent to your email.")

    def log_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Add logic to handle login here
        print(f"Username: {username}, Password: {password}")


if __name__ == "__main__":
    app = ctk.CTk()  # This creates the main window
    app.title("Hotel Management System")
    app.geometry("1024x738")
    login_page = LogInPage(app, controller=None)
    login_page.pack(fill="both", expand=True)