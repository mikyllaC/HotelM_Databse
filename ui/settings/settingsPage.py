# ============== Imports ==============
import customtkinter as ctk
from tkinter import messagebox, ttk

from models.auth import AuthModel
from models.settings import SettingsModel
from utils.session import Session
from utils.helpers import log


# ============== Settings Page ==============
class SettingsPage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)
    TREE_SELECT_COLOR = "#DEECF7"
    BUTTON_COLOR = "#206AA1"

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#F5F5F5")
        self.settings_model = SettingsModel()

        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        # ---- Main Container ----
        main_frame = ctk.CTkFrame(self, fg_color="#F5F5F5")
        main_frame.pack(expand=True, fill="both", padx=0, pady=0)

        # ---- Create Notebook for Tabs ----
        style = ttk.Style(self)
        style.configure("TNotebook", background=self.BG_COLOR_1, borderwidth=0, tabmargins=[0, 0, 0, 0])
        style.configure("TNotebook.Tab", background=self.BG_COLOR_1, foreground=self.TITLE_COLOR,
                        font=("Roboto Condensed", 16, "bold"), padding=[30, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", self.BG_COLOR_2)],
                  foreground=[("selected", self.TITLE_COLOR)],
                  font=[("selected", ("Roboto Condensed", 16, "bold"))])
        style.layout("TNotebook.Tab", [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both", padx=0, pady=0)

        self.create_user_settings_tab()
        self.create_billing_settings_tab()
        self.create_hotel_management_tab()

    def create_user_settings_tab(self):
        """Create the user settings tab for password management"""
        user_frame = ctk.CTkFrame(self.notebook, fg_color="white")
        self.notebook.add(user_frame, text="User Settings")

        # Scrollable content
        scrollable = ctk.CTkScrollableFrame(user_frame, fg_color="white")
        scrollable.pack(expand=True, fill="both", padx=20, pady=20)

        # ---- Title ----
        title_label = ctk.CTkLabel(scrollable, text="User Settings",
                                  font=("Roboto Condensed", 20, "bold"),
                                  text_color="#303644")
        title_label.pack(anchor="w", pady=(0, 20))

        # ---- User Info Section ----
        user_info_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        user_info_frame.pack(fill="x", pady=(0, 10))

        # ---- User Info ----
        user_info = ""
        if Session.current_user:
            full_name = f"{Session.current_user.get('FIRST_NAME', 'Unknown')} {Session.current_user.get('LAST_NAME', 'Unknown')}"
            user_info = f"Logged in as: {full_name} ({Session.current_user.get('EMAIL', 'No email')})"
        else:
            user_info = "Not logged in"

        user_info_label = ctk.CTkLabel(user_info_frame, text=user_info,
                                      font=("Roboto", 12, "bold"), text_color="#303644")
        user_info_label.pack(anchor="w", padx=15, pady=(10, 10))

        # ---- Logout Button Section ----
        logout_container = ctk.CTkFrame(scrollable, fg_color="transparent")
        logout_container.pack(fill="x", pady=(0, 20))

        # ---- Logout Button ----
        logout_btn = ctk.CTkButton(logout_container, text="Log Out",
                                  command=self.handle_logout,
                                  fg_color="#dc3545", hover_color="#c82333",
                                  width=200, height=35)
        logout_btn.pack(pady=5, anchor="w")

        # ---- Divider ----
        divider = ctk.CTkFrame(scrollable, height=2, fg_color="#e0e0e0")
        divider.pack(fill="x", pady=20)

        # ---- Session Section ----
        session_title_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        session_title_frame.pack(fill="x", pady=(0, 5))

        session_label = ctk.CTkLabel(session_title_frame, text="Password Management",
                                    font=("Roboto", 14, "bold"), text_color="#303644")
        session_label.pack(anchor="w")

        # ---- Password Change Section ----
        password_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        password_frame.pack(fill="x", pady=(0, 20))

        # ---- Current Password ----
        self.create_password_field(password_frame, "CURRENT_PASSWORD", "Current Password", is_password=True)
        self.old_pass_input = self.password_fields["CURRENT_PASSWORD"]

        # ---- New Password ----
        self.create_password_field(password_frame, "NEW_PASSWORD", "New Password", is_password=True)
        self.new_pass_input = self.password_fields["NEW_PASSWORD"]

        # ---- Confirm Password ----
        self.create_password_field(password_frame, "CONFIRM_PASSWORD", "Confirm New Password", is_password=True)
        self.confirm_pass_input = self.password_fields["CONFIRM_PASSWORD"]

        # Change password button frame
        save_btn_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        save_btn_frame.pack(fill="x", pady=10)

        # ---- Submit Button ----
        save_btn = ctk.CTkButton(save_btn_frame, text="Change Password",
                                command=self.handle_change_password,
                                fg_color="#206AA1", width=200, height=35)
        save_btn.pack(anchor="w")

        # ---- Divider ----
        divider = ctk.CTkFrame(scrollable, height=1, fg_color="#e0e0e0")
        divider.pack(fill="x", pady=20)

    def create_password_field(self, parent, key, label, is_password=False):
        """Create a password field similar to hotel field style"""
        if not hasattr(self, 'password_fields'):
            self.password_fields = {}

        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=15, pady=5)

        # Label
        label_widget = ctk.CTkLabel(field_frame, text=label + ":",
                                   font=("Roboto", 12), text_color="#303644")
        label_widget.pack(side="left", anchor="w")

        # Input field
        widget = ctk.CTkEntry(field_frame, width=300, height=28,
                             font=("Roboto", 11), show="*" if is_password else "")
        self.password_fields[key] = widget

        widget.pack(side="right", padx=(10, 0))

    def create_billing_settings_tab(self):
        """Tab for billing and financial settings"""
        tab_frame = ctk.CTkFrame(self.notebook, fg_color="white")
        self.notebook.add(tab_frame, text='Billing Settings')

        # Simple scrollable frame
        scrollable = ctk.CTkScrollableFrame(tab_frame, fg_color="white")
        scrollable.pack(expand=True, fill="both", padx=20, pady=20)

        self.billing_settings = {}

        # Simple title
        title_label = ctk.CTkLabel(scrollable, text="Billing & Financial Settings",
                                  font=("Roboto Condensed", 20, "bold"),
                                  text_color="#303644")
        title_label.pack(anchor="w", pady=(0, 20))

        # Tax & Service Charges Section
        tax_label = ctk.CTkLabel(scrollable, text="Tax & Service Charges",
                                font=("Roboto", 14, "bold"), text_color="#303644")
        tax_label.pack(anchor="w", pady=(10, 5))

        tax_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        tax_frame.pack(fill="x", pady=(0, 20))

        tax_fields = [
            ("TAX_RATE", "Tax Rate", "0.12", "DECIMAL"),
            ("SERVICE_CHARGE", "Service Charge", "0.10", "DECIMAL")
        ]

        for i, (key, label, default, type_) in enumerate(tax_fields):
            self.create_simple_field(tax_frame, key, label, default, type_, i, self.billing_settings)

        # Additional Fees Section
        fees_label = ctk.CTkLabel(scrollable, text="Additional Fees",
                                 font=("Roboto", 14, "bold"), text_color="#303644")
        fees_label.pack(anchor="w", pady=(20, 5))

        fees_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        fees_frame.pack(fill="x", pady=(0, 20))

        fee_fields = [
            ("LATE_CHECKOUT_FEE", "Late Checkout Fee", "50.00", "DECIMAL"),
            ("EARLY_CHECKIN_FEE", "Early Check-in Fee", "25.00", "DECIMAL"),
            ("NO_SHOW_CHARGE", "No Show Charge", "100.00", "DECIMAL"),
            ("LATE_PAYMENT_FEE", "Late Payment Fee", "25.00", "DECIMAL")
        ]

        for i, (key, label, default, type_) in enumerate(fee_fields):
            self.create_simple_field(fees_frame, key, label, default, type_, i, self.billing_settings)

        # Deposit & Payment Terms Section
        deposit_label = ctk.CTkLabel(scrollable, text="Deposit & Payment Terms",
                                    font=("Roboto", 14, "bold"), text_color="#303644")
        deposit_label.pack(anchor="w", pady=(20, 5))

        deposit_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        deposit_frame.pack(fill="x", pady=(0, 20))

        deposit_fields = [
            ("DEPOSIT_REQUIRED", "Require Deposit", "true", "BOOLEAN"),
            ("DEPOSIT_AMOUNT", "Default Deposit Amount", "50.00", "DECIMAL"),
            ("DEPOSIT_PERCENTAGE", "Deposit Percentage", "20.00", "DECIMAL"),
            ("PAYMENT_GRACE_PERIOD", "Payment Grace Period (Days)", "3", "INTEGER"),
            ("INVOICE_DUE_DAYS", "Invoice Due Days", "30", "INTEGER"),
            ("REFUND_PROCESSING_DAYS", "Refund Processing Days", "7", "INTEGER")
        ]

        for i, (key, label, default, type_) in enumerate(deposit_fields):
            self.create_simple_field(deposit_frame, key, label, default, type_, i, self.billing_settings)

        # Currency Display Section
        currency_label = ctk.CTkLabel(scrollable, text="Currency Display",
                                     font=("Roboto", 14, "bold"), text_color="#303644")
        currency_label.pack(anchor="w", pady=(20, 5))

        currency_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        currency_frame.pack(fill="x", pady=(0, 20))

        currency_fields = [
            ("CURRENCY_SYMBOL", "Currency Symbol", "₱", "TEXT"),
            ("DECIMAL_PLACES", "Decimal Places", "2", "INTEGER")
        ]

        for i, (key, label, default, type_) in enumerate(currency_fields):
            self.create_simple_field(currency_frame, key, label, default, type_, i, self.billing_settings)

        # Simple save button
        save_btn = ctk.CTkButton(scrollable, text="Save Settings",
                                command=self.save_billing_settings,
                                fg_color="#206AA1", width=150, height=35)
        save_btn.pack(pady=20)

    def create_hotel_management_tab(self):
        """Tab for hotel information management"""
        from models.hotel import HotelModel

        tab_frame = ctk.CTkFrame(self.notebook, fg_color="white")
        self.notebook.add(tab_frame, text='Hotel Information')

        # Simple scrollable frame
        scrollable = ctk.CTkScrollableFrame(tab_frame, fg_color="white")
        scrollable.pack(expand=True, fill="both", padx=20, pady=20)

        self.hotel_model = HotelModel()
        self.hotel_fields = {}

        # Simple title
        title_label = ctk.CTkLabel(scrollable, text="Hotel Information",
                                  font=("Roboto Condensed", 20, "bold"),
                                  text_color="#303644")
        title_label.pack(anchor="w", pady=(0, 20))

        # Hotel Basic Information Section
        basic_label = ctk.CTkLabel(scrollable, text="Basic Information",
                                  font=("Roboto", 14, "bold"), text_color="#303644")
        basic_label.pack(anchor="w", pady=(10, 5))

        basic_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        basic_frame.pack(fill="x", pady=(0, 20))

        # Hotel Name
        self.create_hotel_field(basic_frame, "HOTEL_NAME", "Hotel Name", "The Reverie Hotel")

        # Address
        self.create_hotel_field(basic_frame, "ADDRESS", "Address", "123 Main Street, City, Country")

        # Number of Floors
        self.create_hotel_field(basic_frame, "FLOORS", "Number of Floors", "6")

        # Contact Information Section
        contact_label = ctk.CTkLabel(scrollable, text="Contact Information",
                                    font=("Roboto", 14, "bold"), text_color="#303644")
        contact_label.pack(anchor="w", pady=(20, 5))

        contact_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        contact_frame.pack(fill="x", pady=(0, 20))

        # Phone Number
        self.create_hotel_field(contact_frame, "PHONE_NUMBER", "Phone Number", "+1 234 567 8900")

        # Email
        self.create_hotel_field(contact_frame, "EMAIL", "Email Address", "info@hotel.com")

        # Website
        self.create_hotel_field(contact_frame, "WEBSITE", "Website", "www.hotel.com")

        # Additional Information Section
        additional_label = ctk.CTkLabel(scrollable, text="Additional Information",
                                      font=("Roboto", 14, "bold"), text_color="#303644")
        additional_label.pack(anchor="w", pady=(20, 5))

        additional_frame = ctk.CTkFrame(scrollable, fg_color="#f8f9fa")
        additional_frame.pack(fill="x", pady=(0, 20))

        # Logo Path
        self.create_hotel_field(additional_frame, "LOGO_PATH", "Logo Path", "default_logo.png")

        # Button frame
        button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        # Save button
        save_btn = ctk.CTkButton(button_frame, text="Save Hotel Information",
                                command=self.save_hotel_information,
                                fg_color="#206AA1", width=200, height=35)
        save_btn.pack(side="left", padx=(0, 10))

        # Load hotel info
        self.load_hotel_information()

    def create_hotel_field(self, parent, key, label, default_value):
        """Create a hotel information field"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=15, pady=5)

        # Label
        label_widget = ctk.CTkLabel(field_frame, text=label + ":",
                                   font=("Roboto", 12), text_color="#303644")
        label_widget.pack(side="left", anchor="w")

        # Input field
        widget = ctk.CTkEntry(field_frame, width=300, height=28,
                             font=("Roboto", 11))
        widget.insert(0, default_value)
        self.hotel_fields[key] = widget

        widget.pack(side="right", padx=(10, 0))

    def create_simple_field(self, parent, key, label, default_value, field_type, row, storage_dict):
        """Create a simple settings field for general and billing settings"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=15, pady=5)

        # Label
        label_widget = ctk.CTkLabel(field_frame, text=label + ":",
                                   font=("Roboto", 12), text_color="#303644")
        label_widget.pack(side="left", anchor="w")

        # Create appropriate widget based on field type
        if field_type == "BOOLEAN":
            # Use checkbox for boolean values
            var = ctk.BooleanVar(value=(default_value.lower() in ['true', '1', 'yes']))
            widget = ctk.CTkCheckBox(field_frame, text="", variable=var)
            storage_dict[key] = var
        else:
            # Use entry for all other types
            widget = ctk.CTkEntry(field_frame, width=200, height=28,
                                 font=("Roboto", 11))
            widget.insert(0, default_value)
            storage_dict[key] = widget

        widget.pack(side="right", padx=(10, 0))

    def load_hotel_information(self):
        """Load hotel information from database"""
        try:
            hotel_info = self.hotel_model.get_hotel_info(1)  # Assuming hotel ID 1

            if hotel_info:
                for field_key, widget in self.hotel_fields.items():
                    if field_key in hotel_info and hotel_info[field_key]:
                        widget.delete(0, 'end')
                        widget.insert(0, str(hotel_info[field_key]))
        except Exception as e:
            log(f"Error loading hotel information: {str(e)}", "ERROR")

    def save_hotel_information(self):
        """Save hotel information to database"""
        try:
            hotel_data = {}

            for field_key, widget in self.hotel_fields.items():
                value = widget.get().strip()
                if value:  # Only save non-empty values
                    hotel_data[field_key] = value

            # Convert FLOORS to integer if provided
            if 'FLOORS' in hotel_data:
                try:
                    hotel_data['FLOORS'] = int(hotel_data['FLOORS'])
                except ValueError:
                    messagebox.showerror("Error", "Number of floors must be a valid number.")
                    return

            # Update hotel information
            success = self.hotel_model.update_hotel_info(1, hotel_data)  # Assuming hotel ID 1

            if success:
                messagebox.showinfo("Success", "Hotel information saved successfully!")
                log("Hotel information saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save hotel information.")

        except Exception as e:
            log(f"Error saving hotel information: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save hotel information: {str(e)}")

    def load_settings(self):
        """Load current settings from database"""
        try:
            # Load billing settings
            billing_settings = self.settings_model.get_all_billing_settings()

            for setting in billing_settings:
                key = setting[0]  # SETTING_KEY
                value = setting[1]  # SETTING_VALUE
                field_type = setting[2]  # SETTING_TYPE
                description = setting[3]  # DESCRIPTION

                if key in self.billing_settings:
                    widget = self.billing_settings[key]
                    if isinstance(widget, ctk.BooleanVar):
                        widget.set(value.lower() in ['true', '1', 'yes'])
                    elif hasattr(widget, 'delete') and hasattr(widget, 'insert'):
                        widget.delete(0, 'end')
                        widget.insert(0, value)

        except Exception as e:
            log(f"Error loading settings: {str(e)}", "ERROR")

    def save_billing_settings(self):
        """Save billing settings to database"""
        try:
            settings_to_save = {}

            for key, widget in self.billing_settings.items():
                if isinstance(widget, ctk.BooleanVar):
                    value = "true" if widget.get() else "false"
                    field_type = "BOOLEAN"
                else:
                    value = widget.get().strip()
                    if key in ["TAX_RATE", "SERVICE_CHARGE", "LATE_CHECKOUT_FEE", "EARLY_CHECKIN_FEE",
                              "NO_SHOW_CHARGE", "DEPOSIT_AMOUNT", "DEPOSIT_PERCENTAGE", "LATE_PAYMENT_FEE"]:
                        field_type = "DECIMAL"
                    elif key in ["PAYMENT_GRACE_PERIOD", "INVOICE_DUE_DAYS", "REFUND_PROCESSING_DAYS", "DECIMAL_PLACES"]:
                        field_type = "INTEGER"
                    else:
                        field_type = "TEXT"

                settings_to_save[key] = {
                    'value': value,
                    'type': field_type
                }

            # Update settings using the settings model
            success = self.settings_model.update_multiple_billing_settings(settings_to_save)

            if success:
                messagebox.showinfo("Success", "Billing settings saved successfully!")
                log("Billing settings saved successfully")
            else:
                messagebox.showerror("Error", "Some settings could not be saved.")

        except Exception as e:
            log(f"Error saving billing settings: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save billing settings: {str(e)}")

    def reset_billing_settings(self):
        """Reset billing settings to defaults"""
        confirm = messagebox.askyesno("Confirm Reset",
                                     "Are you sure you want to reset all billing settings to their default values?")
        if confirm:
            try:
                success = self.settings_model.reset_to_defaults('billing')
                if success:
                    messagebox.showinfo("Success", "Billing settings reset to defaults!")
                    self.load_settings()  # Reload the interface
                else:
                    messagebox.showerror("Error", "Failed to reset settings.")
            except Exception as e:
                log(f"Error resetting billing settings: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")

    def handle_change_password(self):
        """Handle password change functionality"""
        # Get current user from session
        current_user = Session.current_user
        if not current_user:
            messagebox.showerror("Error", "No user session found.")
            log("[ERROR] Change password failed: No active user session")
            return

        employee_id = current_user.get('EMPLOYEE_ID')
        if not employee_id:
            messagebox.showerror("Error", "Invalid user session.")
            log("[ERROR] Change password failed: Invalid user session")
            return

        auth_model = AuthModel()
        user_auth_data = auth_model.get_user_credentials(employee_id)

        old_pass = self.old_pass_input.get()
        new_pass = self.new_pass_input.get()
        confirm_pass = self.confirm_pass_input.get()

        # Validation
        if not old_pass or not new_pass or not confirm_pass:
            message = "All fields are required."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return

        if new_pass != confirm_pass:
            message = "New password and confirm password do not match."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return

        if old_pass == new_pass:
            message = "New password cannot be the same as your old password."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return

        if not user_auth_data or old_pass != user_auth_data['PASSWORD']:
            message = "Current password is incorrect."
            messagebox.showwarning("Error", message)
            log(f"Change password failed for ({employee_id}): {message}")
            return

        # Update password
        auth_model.update_user_credentials(employee_id, new_pass)
        log(f"Password change successful for employee ID: {employee_id}")
        messagebox.showinfo("Success", "Password updated successfully.")

        # Clear form
        self.old_pass_input.delete(0, 'end')
        self.new_pass_input.delete(0, 'end')
        self.confirm_pass_input.delete(0, 'end')

    def handle_logout(self):
        """Handle user logout"""
        confirm = messagebox.askyesno("Confirm Logout",
                                     "Are you sure you want to log out?")
        if confirm:
            try:
                # Clear current user session
                Session.current_user = None

                log("User logged out successfully.")
                messagebox.showinfo("Success", "You have been logged out successfully.")

                # Close all windows and relaunch the application to return to login screen
                self.master.master.destroy()  # Close the main application window

                # Restart application
                import main
                main.main()

            except Exception as e:
                log(f"Error during logout: {str(e)}", "ERROR")
                messagebox.showerror("Error", f"Failed to log out: {str(e)}")

    def update_ui_for_logout(self):
        """Update UI elements after logout"""
        # Clear password fields
        for key in ["CURRENT_PASSWORD", "NEW_PASSWORD", "CONFIRM_PASSWORD"]:
            if key in self.password_fields:
                self.password_fields[key].delete(0, 'end')

        # Update user info label
        user_info_label = self.nametowidget(self.notebook.tabs()[0]).winfo_children()[0].winfo_children()[1]
        user_info_label.configure(text="Not logged in")

        # Optionally, switch to a different tab or perform other UI updates
        # self.notebook.select(0)  # Switch to the first tab (e.g., Dashboard)
