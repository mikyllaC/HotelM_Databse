import customtkinter as ctk
from tkinter import messagebox

from models.employee import EmployeeModel
from utils.helpers import log
from ui.components.customDropdown import CustomDropdown


class AssignStaffFrame(ctk.CTkFrame):
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

    def __init__(self, parent_popup, parent_page=None, employee_id=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.parent_page = parent_page
        self.employee_id = employee_id
        self.employee_model = EmployeeModel()

        self.entries = {}
        self.create_widgets()

        if employee_id:
            self.load_employee_data(employee_id)

    # ============== Widget Creation ==============
    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self,
                                    fg_color="#F7F7F7",
                                    corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Assign Staff Member", font=("Roboto Condensed", 24), text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Employee ID ==========
        if self.employee_id:
            id_label = ctk.CTkLabel(self, text=f"Employee ID: {self.employee_id}", font=("Roboto Mono", 12, "bold"),
                                    text_color="#5c5c5c")
            id_label.pack(pady=(10, 0))

        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=40, pady=(30, 20), fill="both", expand=True)

        # ========== Employee Name (Read-only) ==========
        name_label = ctk.CTkLabel(form_frame, text="Employee Name", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        name_label.grid(row=0, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.name_display = ctk.CTkLabel(form_frame, text="Loading...", font=("Roboto", 14, "bold"),
                                        text_color="#303644", anchor="w")
        self.name_display.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=10)

        # ========== Current Position (Read-only) ==========
        position_label = ctk.CTkLabel(form_frame, text="Position", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        position_label.grid(row=1, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.position_display = ctk.CTkLabel(form_frame, text="Loading...", font=("Roboto", 14),
                                           text_color="#303644", anchor="w")
        self.position_display.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)

        # ========== Current Assignment (Read-only) ==========
        current_label = ctk.CTkLabel(form_frame, text="Current Assignment", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        current_label.grid(row=2, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.current_assignment_display = ctk.CTkLabel(form_frame, text="Not assigned", font=("Roboto", 14),
                                                      text_color="#888888", anchor="w")
        self.current_assignment_display.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)

        # ========== Separator ==========
        separator = ctk.CTkFrame(form_frame, height=2, fg_color="#E0E0E0")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=(20, 20), pady=(20, 20))

        # ========== New Assignment ==========
        assign_label = ctk.CTkLabel(form_frame, text="New Assignment *", font=("Roboto", 16, "bold"), text_color="#303644")
        assign_label.grid(row=4, column=0, sticky="nw", padx=self.PADX_LABEL, pady=(10, 5))

        # Assignment Type Dropdown (Using CustomDropdown)
        type_label = ctk.CTkLabel(form_frame, text="Assignment Type", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        type_label.grid(row=5, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        self.assignment_type_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=5, column=1,
            options=["Floor", "Department"],
            placeholder="Select Assignment Type",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False,
            entry_name="assignment_type"
        )

        # Assignment Value
        value_label = ctk.CTkLabel(form_frame, text="Assignment Details *", font=self.FONT_LABEL, text_color=self.TEXT_COLOR_LABEL)
        value_label.grid(row=6, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)

        # This will change based on assignment type (Using CustomDropdown)
        self.assignment_value_dropdown = CustomDropdown(
            parent=self, parent_frame=form_frame,
            row=6, column=1,
            options=["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6"],
            placeholder="Select Assignment Details",
            width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT,
            add_new_option=False,
            entry_name="assignment_value"
        )

        # Bind assignment type change to update assignment values
        # We'll monitor the StringVar directly
        self.assignment_type_dropdown.selected_value.trace_add("write", self._on_assignment_type_changed)

        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=7, column=1, pady=(30, 20), sticky="ew")

        # ========== Assign Button ==========
        self.assign_button = ctk.CTkButton(button_frame, text="Assign", command=self.on_assign,
                                          height=35, width=100, fg_color="#28a745", hover_color="#218838")
        self.assign_button.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # ========== Clear Assignment Button ==========
        self.clear_button = ctk.CTkButton(button_frame, text="Clear Assignment", command=self.on_clear_assignment,
                                         height=35, width=120, fg_color="#dc3545", hover_color="#c82333")
        self.clear_button.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # ========== Cancel Button ==========
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.on_cancel,
                                          height=35, width=80, fg_color="#6c757d", hover_color="#545b62")
        self.cancel_button.grid(row=0, column=2, sticky="w")

    def _on_assignment_type_changed(self, *args):
        """Handle assignment type change event"""
        selected_type = self.assignment_type_dropdown.get()
        if selected_type:
            self.on_assignment_type_change(selected_type)

    def on_assignment_type_change(self, selected_type):
        """Update assignment value dropdown based on selected type"""
        if selected_type == "Floor":
            values = ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6"]
        elif selected_type == "Department":
            values = ["Front Desk", "Housekeeping", "Maintenance", "Security", "Kitchen", "Food & Beverage", "Administration"]
        else:
            values = ["Select assignment type first"]

        # Update the dropdown values
        self.assignment_value_dropdown.set_options(values)
        if values and values[0] != "Select assignment type first":
            self.assignment_value_dropdown.set(values[0])

    def load_employee_data(self, employee_id):
        """Load and display employee information"""
        employee = self.employee_model.get_employee_details(employee_id)
        if not employee:
            messagebox.showerror("Error", "Employee not found.")
            return

        # Update display labels
        full_name = f"{employee['FIRST_NAME']} {employee['LAST_NAME']}"
        self.name_display.configure(text=full_name)
        self.position_display.configure(text=employee['POSITION'])

        current_assignment = employee.get('ASSIGNED_TO', '')
        if current_assignment:
            self.current_assignment_display.configure(text=current_assignment, text_color="#303644")
        else:
            self.current_assignment_display.configure(text="Not assigned", text_color="#888888")

    def on_assign(self):
        """Handle assignment of staff member"""
        if not self.employee_id:
            messagebox.showerror("Error", "No employee selected.")
            return

        # Get assignment details from dropdown selections
        assignment_type = self.assignment_type_dropdown.get()
        assignment_value = self.assignment_value_dropdown.get()

        if not assignment_type or not assignment_value or assignment_value == "Select assignment type first":
            messagebox.showerror("Validation Error", "Please select both assignment type and assignment details.")
            return

        new_assignment = f"{assignment_type}: {assignment_value}"

        try:
            # Update the employee's assignment
            success = self.employee_model.assign_staff(self.employee_id, new_assignment)

            if success:
                messagebox.showinfo("Success", f"Staff member successfully assigned to:\n{new_assignment}")

                # Refresh parent page if available
                if self.parent_page:
                    self.parent_page.populate_employee_data()

                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to assign staff member. Employee may not exist.")

        except Exception as e:
            log(f"Error assigning staff: {str(e)}")
            messagebox.showerror("Error", f"Failed to assign staff member: {e}")

    def on_clear_assignment(self):
        """Clear the employee's current assignment"""
        if not self.employee_id:
            messagebox.showerror("Error", "No employee selected.")
            return

        # Confirm action
        confirm = messagebox.askyesno("Confirm Clear Assignment",
                                     "Are you sure you want to clear this employee's assignment?")
        if not confirm:
            return

        try:
            # Clear assignment by setting it to empty string
            success = self.employee_model.assign_staff(self.employee_id, "")

            if success:
                messagebox.showinfo("Success", "Staff assignment cleared successfully.")

                # Refresh parent page if available
                if self.parent_page:
                    self.parent_page.populate_employee_data()

                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to clear assignment. Employee may not exist.")

        except Exception as e:
            log(f"Error clearing staff assignment: {str(e)}")
            messagebox.showerror("Error", f"Failed to clear assignment: {e}")

    def on_cancel(self):
        """Cancel and close the dialog"""
        self.master.destroy()
