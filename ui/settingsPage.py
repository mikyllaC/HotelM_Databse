# ============== Imports ==============
import customtkinter as ctk
from tkinter import messagebox


# ============== Settings Page ==============
class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#e6e6e6")

        # ============== Main Layout ==============

        # ---- Outer Container ----
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.configure(fg_color="transparent")
        self.label_frame.pack(padx=40, pady=40, fill='both', expand=True)

        # ---- Title ----
        ctk.CTkLabel(self.label_frame, text="Settings", font=("Arial", 23, "bold")).pack(pady=(0, 10), anchor='w')
       
        # ---- Top Separator ----
        ctk.CTkFrame(self.label_frame, height=2, fg_color="#cccccc").pack(fill='x', pady=(0, 20))
        
        # ---- Form Section ----
        form_frame = ctk.CTkFrame(self.label_frame, fg_color="transparent")
        form_frame.pack(anchor='w', padx=20, pady=10, fill='x')

        ctk.CTkLabel(form_frame, text="Reset your Password", font=("Arial", 17, "bold")).pack(anchor='w', pady=(0, 20))

        # ============== Password Fields ==============

        # ---- Current Password ----
        ctk.CTkLabel(form_frame, text="Current Password:").pack(anchor='w', pady=(10, 0))
        self.old_pass_input = ctk.CTkEntry(form_frame, show="*")
        self.old_pass_input.pack(anchor='w', padx=0, pady=5)

        # ---- New and Confirm Password (Side by Side) ----
        password_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_row.pack(anchor='w', pady=(10, 0), fill='x')

        # ---- New Password ----
        new_pass_col = ctk.CTkFrame(password_row, fg_color="transparent")
        new_pass_col.pack(side='left', padx=(0, 10))
        ctk.CTkLabel(new_pass_col, text="New Password:").pack(anchor='w', pady=(0, 2))
        self.new_pass_input = ctk.CTkEntry(new_pass_col, show="*")
        self.new_pass_input.pack(anchor='w', pady=5)

        # ---- Confirm Password ----
        confirm_pass_col = ctk.CTkFrame(password_row, fg_color="transparent")
        confirm_pass_col.pack(side='left', padx=(0, 0))
        ctk.CTkLabel(confirm_pass_col, text="Confirm New Password:").pack(anchor='w', pady=(0, 2))
        self.confirm_pass_input = ctk.CTkEntry(confirm_pass_col, show="*")
        self.confirm_pass_input.pack(anchor='w', pady=5)

        # ---- Submit Button ----
        ctk.CTkButton(form_frame, text="Change Password", command=self.handle_change_password).pack(anchor='w', pady=20)
        
        # ---- Bottom Separator ----
        ctk.CTkFrame(self.label_frame, height=2, fg_color="#cccccc").pack(fill='x', pady=(0, 20))


    # ============== Events ==============
    def handle_change_password(self):
        # Validates and updates the password
        old_pass = self.old_pass_input.get()
        new_pass = self.new_pass_input.get()
        confirm_pass = self.confirm_pass_input.get()

        if not old_pass or not new_pass or not confirm_pass:
            messagebox.showwarning("Error", "All fields are required.")
            return

        if new_pass != confirm_pass:
            messagebox.showwarning("Error", "New passwords do not match.")
            return

        # --- Simulated backend check ---
        if old_pass == "current_password":
            messagebox.showinfo("Success", "Password changed successfully.")
            self.old_pass_input.delete(0, 'end')
            self.new_pass_input.delete(0, 'end')
            self.confirm_pass_input.delete(0, 'end')
        else:
            messagebox.showwarning("Error", "Current password is incorrect.")