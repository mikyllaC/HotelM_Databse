# ============== Imports ==============
import customtkinter as ctk
from tkinter import messagebox

from database.db_manager import DBManager
from utils.session import Session
from utils.helpers import log


# ============== Settings Page ==============
class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widget()


    # ============== Widget Creation ==============
    def create_widget(self):
        self.configure(fg_color="#f0f0f0")
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

        # ---- Frame: New and Confirm Password (Side by Side) ----
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
        employee_id = getattr(Session.current_user, 'employee_id', 'None')
        if not employee_id:
            messagebox.showerror("Error", "No user session found.")
            log("[ERROR] Change password failed: No active user session")

        db = DBManager()
        user_auth_data = db.get_user_credentials(employee_id)

        old_pass = self.old_pass_input.get()
        new_pass = self.new_pass_input.get()
        confirm_pass = self.confirm_pass_input.get()

        if not old_pass or not new_pass or not confirm_pass:
            message = "All fields are required."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return
        if new_pass != confirm_pass:
            message = "New password and confirm password does not match."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return
        if old_pass == new_pass:
            message = "New password cannot be the same as your old password."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return
        if old_pass != user_auth_data['PASSWORD']:
            message = "Old password is incorrect."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return

        db.update_user_credentials(employee_id, new_pass)
        log(f"Password change successful for employee ID: {employee_id}")
        messagebox.showinfo("Success", "Password updated successfully.")

        self.old_pass_input.delete(0, 'end')
        self.new_pass_input.delete(0, 'end')
        self.confirm_pass_input.delete(0, 'end')