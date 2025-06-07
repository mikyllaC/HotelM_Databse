import customtkinter as ctk
import datetime
from tkinter import messagebox

from models.employee import EmployeeModel


class EditStaffFrame(ctk.CTkFrame):
    def __init__(self, parent_popup, employee_id, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.employee_id = employee_id
        self.parent_page = parent_page
        self.employee_model = EmployeeModel()
        self.fields = {}

        self.employee_data = self.employee_model.get_employee_details(employee_id)

        if not self.employee_data:
            messagebox.showerror("Error", f"Employee ID {employee_id} not found.")
            self.master.destroy()
            return

        self.create_scrollable_widgets()


    def create_scrollable_widgets(self):
        ctk.CTkLabel(self, text="Edit Staff Details", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        # Scrollable Frame
        scroll_frame = ctk.CTkScrollableFrame(self, width=500, height=500)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Field definitions
        field_defs = [
            ("First Name", "FIRST_NAME", "entry"),
            ("Last Name", "LAST_NAME", "entry"),
            ("Gender", "GENDER", "dropdown", ["Male", "Female", "Other"]),
            ("Contact Number", "CONTACT_NUMBER", "entry"),
            ("Email", "EMAIL", "entry"),
            ("Date of Birth (YYYY-MM-DD)", "DATE_OF_BIRTH", "entry"),
            ("Address", "ADDRESS", "entry"),
            ("Role", "POSITION", "dropdown", ["CEO", "Manager", "Cleaner", "Receptionist", "Chef", "Security"]),
            ("Hire Date (YYYY-MM-DD)", "HIRE_DATE", "entry"),
            ("Salary", "SALARY", "entry"),
            ("Status", "STATUS", "dropdown", ["Available", "Terminated", "On Leave", "Suspended", "Retired"]),
        ]

        for label_text, key, field_type, *options in field_defs:
            ctk.CTkLabel(scroll_frame, text=label_text, anchor="w").pack(fill="x", pady=(10, 2))

            if field_type == "entry":
                entry = ctk.CTkEntry(scroll_frame)
                entry.insert(0, str(self.employee_data.get(key, "")))
                entry.pack(fill="x")
                self.fields[key] = entry

            elif field_type == "dropdown":
                values = options[0]
                combo = ctk.CTkOptionMenu(scroll_frame, values=values)
                current_value = self.employee_data.get(key, values[0])
                if current_value in values:
                    combo.set(current_value)
                else:
                    combo.set(values[0])
                combo.pack(fill="x")
                self.fields[key] = combo

        # Button Frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", command=self.save_changes)
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", command=self.master.destroy)
        cancel_btn.pack(side="left", padx=10)


    def save_changes(self):
        updated_data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, ctk.CTkOptionMenu):
                value = widget.get().strip()
            else:
                value = widget.get().strip()

            if not value:
                messagebox.showwarning("Validation Error",
                                       f"{key.replace('_', ' ').title()} cannot be empty.")
                return
            updated_data[key] = value

        try:
            # Date validation
            if "DOB" in updated_data:
                datetime.datetime.strptime(updated_data["DOB"], "%Y-%m-%d")
            if "HIRE_DATE" in updated_data:
                datetime.datetime.strptime(updated_data["HIRE_DATE"], "%Y-%m-%d")

            # Salary validation
            if "SALARY" in updated_data:
                updated_data["SALARY"] = float(updated_data["SALARY"])

            # Update DB
            self.employee_model.update_employee_details(self.employee_id, updated_data)
            messagebox.showinfo("Success", "Staff details updated successfully.")
            if self.parent_page:
                self.parent_page.populate_staff_list()  # refreshes tree after update
            self.master.destroy()

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update employee.\n{str(e)}")
