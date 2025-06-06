import customtkinter as ctk
from tkinter import messagebox

from models.employee import EmployeeModel
from utils.helpers import log


class AssignStaffFrame(ctk.CTkFrame):
    def __init__(self, parent_popup, employee_id, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color="white")
        self.employee_id = employee_id
        self.parent_page = parent_page
        self.employee_model = EmployeeModel()

        self.create_widgets()


    def create_widgets(self):
        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, weight=0)
        #self.rowconfigure((0,2), weight=1)
        #self.rowconfigure(1, weight=0)

        content_frame = ctk.CTkFrame(self, fg_color="white")
        content_frame.grid(column=1,row=1)

        upper_frame = ctk.CTkFrame(content_frame, fg_color="white")
        upper_frame.grid(row=0)

        ctk.CTkLabel(upper_frame, text="Assign Staff to Room", font=("Arial", 16, "bold")).grid(row=0, pady=(20, 10))

        ctk.CTkLabel(upper_frame, text="Staff ID:", font=("Arial", 13)).grid(row=1, pady=(5, 0))
        self.staff_entry = ctk.CTkEntry(upper_frame, width=220)
        self.staff_entry.insert(0, self.employee_id)
        self.staff_entry.grid(row=2, pady=5)

        ctk.CTkLabel(upper_frame, text="Room/Floor:", font=("Arial", 13)).grid(row=3, pady=(10, 0))
        room_options = ["None"] + [f"Floor {i}" for i in range(1, 13)]
        self.room_var = ctk.StringVar(value=room_options[0])
        # value=room_options[0]: sets the initial selected value to "Floor 1" (the first item in the list)

        room_dropdown = ctk.CTkComboBox(upper_frame, variable=self.room_var, values=room_options,
                                            width=220, height=32, font=("Courier", 13))
        room_dropdown.grid(row=4, pady=5)

        lower_frame = ctk.CTkFrame(content_frame, fg_color="white")
        lower_frame.grid(row=1,pady=(35, 15),padx=5)

        assign_button = ctk.CTkButton(lower_frame, text="Assign", width=80,
                                      command=self.save_changes)
        assign_button.grid(column=0,row=1, padx=(10, 10))

        cancel_button = ctk.CTkButton(lower_frame, text="Cancel", fg_color="gray", width=80,
                                      command=self.master.destroy)
        cancel_button.grid(column=1,row=1, padx=(10, 10))


    def save_changes(self):
        staff_id = self.staff_entry.get().strip()
        assigned_to = self.room_var.get()

        if not staff_id:
            messagebox.showerror(title="Error", message="Staff ID cannot be empty.")
            return

        if assigned_to == "None":
            assigned_to = None

        success = self.employee_model.assign_staff(employee_id=staff_id, assigned_to=assigned_to)
        if success:
            log(f"Assigned staff {staff_id} to {assigned_to}.")
            if self.parent_page:
                self.parent_page.populate_staff_list()  # refreshes tree after update
            self.master.destroy()