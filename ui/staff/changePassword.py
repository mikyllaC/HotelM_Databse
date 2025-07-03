# ============== Imports ==============
import customtkinter as ctk
from tkinter import messagebox

from PIL.ImageOps import expand

from models.auth import AuthModel
from models.employee import EmployeeModel
from utils.helpers import log


# ============== Change Password Frame ==============
class ChangePasswordFrame(ctk.CTkFrame):
    FONT_LABEL = ("Roboto", 14)
    FONT_ENTRY = ("Roboto", 10)
    FONT_ENTRY_LABEL = ("Roboto", 12)
    TEXT_COLOR_LABEL = "black"
    TEXT_COLOR_ENTRY = "#818197"
    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    PADX_LABEL = (20, 80)
    BG_COLOR_2 = "white"

    def __init__(self, parent_popup, parent_page, employee_id):
        super().__init__(parent_popup)
        self.configure(fg_color="white")

        self.parent_popup = parent_popup
        self.parent_page = parent_page
        self.employee_id = employee_id

        self.auth_model = AuthModel()
        self.employee_model = EmployeeModel()

        # Get employee details
        self.employee_info = self.employee_model.get_employee_details(employee_id)

        self.create_widgets()

        # Set focus to new password entry after window loads
        self.after(100, lambda: self.entries["entry_new_password"].focus_set())


    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self,
                                    fg_color="#F7F7F7",
                                    corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Change Password", font=("Roboto Condensed", 24), text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Employee ID ==========
        if self.employee_info:
            employee_name = f"{self.employee_info['FIRST_NAME']} {self.employee_info['LAST_NAME']}"
            id_label = ctk.CTkLabel(self, text=f"Employee: {employee_name} ({self.employee_id})",
                                    font=("Roboto Mono", 12, "bold"),
                                    text_color="#5c5c5c")
            id_label.pack(pady=(10, 0))

        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(30, 20), fill="both", expand=True)

        # Store entry references
        self.entries = {}

        # ========== New Password ==========
        new_password_label = ctk.CTkLabel(form_frame, text="New Password *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        new_password_label.grid(row=0, column=0, sticky="nw", padx=self.PADX_LABEL, pady=(0, 10))

        entry_new_password = ctk.CTkEntry(form_frame,
                                         width=self.ENTRY_WIDTH,
                                         height=self.ENTRY_HEIGHT,
                                         border_width=self.BORDER_WIDTH,
                                         border_color=self.BORDER_COLOR)
        entry_new_password.grid(row=0, column=1, sticky="w", pady=(0, 10))
        self.entries["entry_new_password"] = entry_new_password
        entry_new_password.bind('<Return>', lambda e: self.entries["entry_confirm_password"].focus_set())

        # ========== Confirm Password ==========
        confirm_password_label = ctk.CTkLabel(form_frame, text="Confirm Password *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        confirm_password_label.grid(row=1, column=0, sticky="nw", padx=self.PADX_LABEL, pady=(0, 10))

        entry_confirm_password = ctk.CTkEntry(form_frame,
                                             width=self.ENTRY_WIDTH,
                                             height=self.ENTRY_HEIGHT,
                                             border_width=self.BORDER_WIDTH,
                                             border_color=self.BORDER_COLOR)
        entry_confirm_password.grid(row=1, column=1, sticky="w", pady=(0, 10))
        self.entries["entry_confirm_password"] = entry_confirm_password
        entry_confirm_password.bind('<Return>', self.change_password)

        # ========== Password Requirements Info ==========
        info_frame = ctk.CTkFrame(form_frame, fg_color="#F0F8FF", corner_radius=5,
                                 border_width=1, border_color="#B0C4DE")
        info_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20), padx=(20, 0))

        info_label = ctk.CTkLabel(info_frame,
                                 text="Password Requirements:\n• Minimum 6 characters\n• Passwords must match",
                                 font=self.FONT_ENTRY_LABEL,
                                 text_color="#4682B4",
                                 justify="left")
        info_label.pack(pady=10, padx=15)

        # ========== Action Buttons ==========
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=40, pady=(0, 30))

        # Create a centered button container
        button_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_container.pack(expand=True)

        # Cancel button
        cancel_button = ctk.CTkButton(button_container,
                                      text="Cancel",
                                      width=120,
                                      height=35,
                                      font=("Roboto", 14),
                                      fg_color="transparent",
                                      text_color="#64748b",
                                      hover_color="#f1f5f9",
                                      border_width=self.BORDER_WIDTH,
                                      border_color=self.BORDER_COLOR,
                                      command=self.cancel_change)
        cancel_button.pack(side="left", padx=(0, 10))

        # Change Password button
        self.change_button = ctk.CTkButton(button_container,
                                           text="Change Password",
                                           width=150,
                                           height=35,
                                           font=("Roboto", 14),
                                           fg_color="#2E8B57",
                                           hover_color="#228B22",
                                           command=self.change_password)
        self.change_button.pack(side="left", padx=(10, 0))

        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)

    def validate_passwords(self):
        """Validate password requirements"""
        new_password = self.entries["entry_new_password"].get().strip()
        confirm_password = self.entries["entry_confirm_password"].get().strip()

        errors = []

        # Check if passwords are provided
        if not new_password:
            errors.append("New password is required")
        if not confirm_password:
            errors.append("Password confirmation is required")

        # Check minimum length
        if len(new_password) < 6:
            errors.append("Password must be at least 6 characters long")

        # Check if passwords match
        if new_password and confirm_password and new_password != confirm_password:
            errors.append("Passwords do not match")

        return errors


    def change_password(self, event=None):
        """Handle password change process"""
        # Validate passwords
        errors = self.validate_passwords()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        new_password = self.entries["entry_new_password"].get().strip()

        # Confirm action
        if self.employee_info:
            employee_name = f"{self.employee_info['FIRST_NAME']} {self.employee_info['LAST_NAME']}"
            confirm_msg = f"Are you sure you want to change the password for {employee_name} ({self.employee_id})?"
        else:
            confirm_msg = f"Are you sure you want to change the password for {self.employee_id}?"

        if not messagebox.askyesno("Confirm Password Change", confirm_msg):
            return

        try:
            # Update password using AuthModel
            self.auth_model.update_user_credentials(self.employee_id, new_password)

            # Success message
            messagebox.showinfo("Success", "Password changed successfully!")
            log(f"Password changed successfully for employee: {self.employee_id}")

            # Close the popup
            self.parent_popup.destroy()

        except Exception as e:
            error_msg = f"Failed to change password: {str(e)}"
            messagebox.showerror("Error", error_msg)
            log(f"Password change error for {self.employee_id}: {str(e)}")


    def cancel_change(self):
        """Handle cancel action"""
        # Ask for confirmation if fields have content
        if (self.entries["entry_new_password"].get().strip() or
            self.entries["entry_confirm_password"].get().strip()):
            if messagebox.askyesno("Cancel Changes", "Are you sure you want to cancel? Any changes will be lost."):
                self.parent_popup.destroy()
        else:
            self.parent_popup.destroy()


# ========== Preview Frame as App ==========
if __name__ == "__main__":
    # For testing purposes
    root = ctk.CTk()
    root.title("Change Password")
    root.geometry("400x300")

    # Mock popup window for testing
    popup = ctk.CTkToplevel(root)
    popup.title("Change Password")
    popup.geometry("400x500")

    frame = ChangePasswordFrame(popup, None, "SM0001")  # Test with employee ID
    frame.pack(fill="both", expand=True)

    root.mainloop()
