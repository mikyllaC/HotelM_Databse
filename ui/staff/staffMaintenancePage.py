# ============== Imports ==============
import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

from models.employee import EmployeeModel
from utils.helpers import log


# ============== Staff Maintenance Page ==============
class StaffMaintenancePage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.employee_model = EmployeeModel()
        self.employee_data = [["Employee ID", "Name", "Position", "Phone", "Email", "Assigned To", "Status"]]

        self.create_widgets()
        self.populate_employee_data()


# ============== Widget Creation ==============
    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Staff Management", font=("Roboto Condensed", 28, "bold"),
                                   text_color="#303644")
        title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))

        # Action Bar Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(anchor="n", padx=(35, 0), fill="x")

        # Add Staff Button
        add_staff_button = ctk.CTkButton(
            self.action_frame,
            text="Add Staff",
            font=("Arial", 16, "bold"),
            width=150,
            height=36,
            command=self.add_staff_popup
        )
        add_staff_button.pack(side="left", padx=(0, 10))

        # Search Entry
        self.search_var = StringVar()
        self.search_entry = ctk.CTkEntry(
            self.action_frame,
            width=220,
            height=36,
            placeholder_text="Search staff name...",
            textvariable=self.search_var,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.action_frame,
            width=160,
            height=36,
            values=["All Status", "Active", "Inactive", "On Leave"],
            variable=self.filter_var,
            font=("Arial", 14)
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.filter_table())

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(15, 10), fill="both", expand=True, anchor="n")

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2, corner_radius=0,
                                        border_width=1, border_color=self.BORDER_COLOR)
        self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.25, relheight=1)
        # Initially hidden
        self.right_frame.place_forget()

        # Treeview for Employee Data
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=25, font=self.TREE_FONT, anchor="w")

        self.treeview = ttk.Treeview(self.table_frame,
                                     columns=["Employee ID", "Name", "Position", "Phone",
                                              "Email", "Assigned To", "Status"],
                                     show="headings")
        self.treeview.pack(expand=True, fill="both")

        for col in self.employee_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w")

        # Set the column widths
        self.treeview.column("Employee ID", width=60, anchor="w")
        self.treeview.column("Name", width=150, anchor="w")
        self.treeview.column("Position", width=100, anchor="w")
        self.treeview.column("Phone", width=100, anchor="w")
        self.treeview.column("Email", width=200, anchor="w")
        self.treeview.column("Assigned To", width=180, anchor="w")
        self.treeview.column("Status", width=80, anchor="w")

        self.update_treeview()
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)


# ========== Events ==========

    def populate_employee_data(self):
        employee_data = self.employee_model.get_all_employees()

        if not employee_data:
            self.employee_data = [["Employee ID", "Name", "Position", "Phone", "Email", "Assigned To", "Status"],
                                  ["-", "-", "-", "-", "-", "-", "-"]]
        else:
            self.employee_data = [["Employee ID", "Name", "Position", "Phone", "Email", "Assigned To", "Status"]] + [
                [row['EMPLOYEE_ID'], f"{row['FIRST_NAME']} {row['LAST_NAME']}",
                 row['POSITION'], row['CONTACT_NUMBER'], row['EMAIL'],
                 row['ASSIGNED_TO'] or "Not assigned",
                 row['STATUS']]
                for row in employee_data
            ]

        self.update_treeview()

    def filter_table(self):
        search_text = self.search_var.get().lower()
        selected_status = self.filter_var.get()

        filtered_data = [self.employee_data[0]]
        for row in self.employee_data[1:]:
            name = row[1].lower() if len(row) > 1 else ""
            status = row[6] if len(row) > 6 else ""
            if (search_text in name) and (selected_status == "All Status" or status == selected_status):
                filtered_data.append(row)

        self.update_treeview(filtered_data)

    def update_treeview(self, data=None):
        if data is None:
            data = self.employee_data

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Process the data excluding the header
        for row in data[1:]:
            employee_id = row[0]  # Employee ID for selection
            self.treeview.insert("", "end", iid=employee_id, values=row)

    def show_employee_info(self, employee_info):
        # Clear previous widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.current_employee_index = next(
            (i for i, row in enumerate(self.employee_data[1:]) if str(row[0]) == str(employee_info['EMPLOYEE_ID'])), None)

        # Header
        self.right_frame.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                    border_width=1, border_color=self.BORDER_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # Left Header Frame for navigation
        left_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        left_header_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

        # Navigation buttons
        def go_to_previous_employee():
            if self.current_employee_index is not None and self.current_employee_index > 0:
                self.current_employee_index -= 1
                employee_id = self.employee_data[self.current_employee_index + 1][0]
                self.treeview.selection_set(employee_id)
                self.treeview.see(employee_id)
                employee_info = self.employee_model.get_employee_details(employee_id)
                if employee_info:
                    self.show_employee_info(employee_info)

        def go_to_next_employee():
            if self.current_employee_index is not None and self.current_employee_index < len(self.employee_data) - 2:
                self.current_employee_index += 1
                employee_id = self.employee_data[self.current_employee_index + 1][0]
                self.treeview.selection_set(employee_id)
                self.treeview.see(employee_id)
                employee_info = self.employee_model.get_employee_details(employee_id)
                if employee_info:
                    self.show_employee_info(employee_info)

        previous_button = ctk.CTkButton(left_header_frame, text="<", text_color="black", width=30, height=30,
                                        corner_radius=4, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR,
                                        font=("Roboto", 20), command=go_to_previous_employee)
        previous_button.grid(column=0, row=0, padx=(10, 5))

        next_button = ctk.CTkButton(left_header_frame, text=">", text_color="black", width=30, height=30,
                                    corner_radius=4, fg_color=self.BG_COLOR_2,
                                    border_width=1, border_color=self.BORDER_COLOR,
                                    font=("Roboto", 20), command=go_to_next_employee)
        next_button.grid(column=1, row=0, padx=(0, 10))

        # Right Header Frame for actions
        right_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        right_header_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="e")

        # Edit and Exit Buttons
        edit_button = ctk.CTkButton(right_header_frame, text="Edit", text_color="black", width=50, height=30,
                                    corner_radius=4, fg_color=self.BG_COLOR_2,
                                    border_width=1, border_color=self.BORDER_COLOR,
                                    command=self.edit_staff_popup)
        edit_button.grid(column=0, row=0, padx=(0, 5))

        assign_button = ctk.CTkButton(right_header_frame, text="Assign", text_color="black", width=60, height=30,
                                      corner_radius=4, fg_color=self.BG_COLOR_2,
                                      border_width=1, border_color=self.BORDER_COLOR,
                                      command=self.assign_staff_popup)
        assign_button.grid(column=1, row=0, padx=(0, 5))

        # Change Password Button
        password_button = ctk.CTkButton(right_header_frame, text="Change Password", text_color="black", width=70, height=30,
                                       corner_radius=4, fg_color=self.BG_COLOR_2,
                                       border_width=1, border_color=self.BORDER_COLOR,
                                       command=self.change_password_popup)
        password_button.grid(column=2, row=0, padx=(0, 5))

        # Delete Staff Button
        delete_button = ctk.CTkButton(right_header_frame, text="Delete", text_color="white", width=60, height=30,
                                      corner_radius=4, fg_color="#dc3545", hover_color="#c82333",
                                      border_width=1, border_color=self.BORDER_COLOR,
                                      command=self.delete_staff)
        delete_button.grid(column=3, row=0, padx=(0, 5))

        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                    corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                    command=lambda: [self.right_frame.place_forget(),
                                                     self.treeview.selection_remove(self.treeview.selection()),
                                                     setattr(self, 'current_employee_index', None)],
                                    font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=4, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Title
        title_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Employee Overview", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Employee Information
        content_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2)
        content_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        full_name = f"{employee_info['FIRST_NAME']} {employee_info['LAST_NAME']}"

        # Add information rows
        info_rows = [
            ("Employee ID", employee_info['EMPLOYEE_ID']),
            ("Name", full_name),
            ("Gender", employee_info['GENDER']),
            ("Phone", employee_info['CONTACT_NUMBER']),
            ("Email", employee_info['EMAIL']),
            ("Date of Birth", employee_info['DATE_OF_BIRTH']),
            ("Address", employee_info['ADDRESS']),
            ("Position", employee_info['POSITION']),
            ("Hire Date", employee_info['HIRE_DATE']),
            ("Salary", f"${employee_info['SALARY']:,.2f}" if employee_info['SALARY'] else "Not set"),
            ("Assigned To", employee_info['ASSIGNED_TO'] or "Not assigned"),
            ("Status", employee_info['STATUS']),
        ]

        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(content_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew", padx=(0, 0), pady=0)

            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w")
            label_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Value "cell" frame
            value_cell = ctk.CTkFrame(content_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            value_cell.grid(row=index, column=1, sticky="nsew", padx=(0, 0), pady=0)

            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                      anchor="w", wraplength=250, justify="left")
            value_text.pack(fill="both", expand=True, padx=10, pady=10)

        content_frame.grid_columnconfigure((0, 1), weight=1, uniform="info")

    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            employee_id = selected_item[0]
            employee_info = self.employee_model.get_employee_details(employee_id)
            if employee_info:
                self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.4, relheight=1)
                self.show_employee_info(employee_info)
        else:
            self.right_frame.place_forget()


# ========== Staff Popups ==========

    def add_staff_popup(self):
        from ui.staff.addStaff import AddStaffFrame

        popup = ctk.CTkToplevel(self)
        popup.title("Add Staff")
        popup.geometry("650x800")
        popup.grab_set()

        frame = AddStaffFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)

    def edit_staff_popup(self):
        from ui.staff.editStaff import EditStaffFrame

        selected_item = self.treeview.selection()
        if selected_item:
            employee_id = selected_item[0]

            popup = ctk.CTkToplevel(self)
            popup.title("Edit Staff")
            popup.geometry("650x850")
            popup.grab_set()

            frame = EditStaffFrame(parent_popup=popup, parent_page=self, employee_id=employee_id)
            frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("No Selection", "Please select a staff member to edit.")
            log("Edit Staff: No staff member selected for editing.")

    def assign_staff_popup(self):
        from ui.staff.assignStaff import AssignStaffFrame

        selected_item = self.treeview.selection()
        if selected_item:
            employee_id = selected_item[0]

            popup = ctk.CTkToplevel(self)
            popup.title("Assign Staff")
            popup.geometry("670x600")
            popup.grab_set()

            frame = AssignStaffFrame(parent_popup=popup, parent_page=self, employee_id=employee_id)
            frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("No Selection", "Please select a staff member to assign.")
            log("Assign Staff: No staff member selected for assignment.")

    def change_password_popup(self):
        from ui.staff.changePassword import ChangePasswordFrame

        selected_item = self.treeview.selection()
        if selected_item:
            employee_id = selected_item[0]

            popup = ctk.CTkToplevel(self)
            popup.title("Change Password")
            popup.geometry("500x400")
            popup.grab_set()

            frame = ChangePasswordFrame(parent_popup=popup, parent_page=self, employee_id=employee_id)
            frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("No Selection", "Please select a staff member to change password.")
            log("Change Password: No staff member selected for password change.")

    def delete_staff(self):
        selected_item = self.treeview.selection()
        if selected_item:
            employee_id = selected_item[0]
            employee_info = self.employee_model.get_employee_details(employee_id)

            if employee_info:
                confirm = messagebox.askyesno("Confirm Deletion",
                                               f"Are you sure you want to delete {employee_info['FIRST_NAME']} {employee_info['LAST_NAME']}? This action cannot be undone.")
                if confirm:
                    # Call the model method to delete the employee
                    success = self.employee_model.delete_employee(employee_id)

                    if success:
                        messagebox.showinfo("Success", "Staff member deleted successfully.")
                        # Update the employee data and treeview
                        self.populate_employee_data()
                        self.right_frame.place_forget()  # Hide the right frame
                    else:
                        messagebox.showerror("Error", "Failed to delete staff member. Please try again.")
            else:
                messagebox.showwarning("No Data", "No staff member data found for the selected item.")
        else:
            messagebox.showwarning("No Selection", "Please select a staff member to delete.")
            log("Delete Staff: No staff member selected for deletion.")


# ========== Preview Frame as App ==========
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Staff Management Page")
    app = StaffMaintenancePage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()