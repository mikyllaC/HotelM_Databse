# ============== Imports ==============
from tkinter import ttk, messagebox
import customtkinter as ctk

from models.employee import EmployeeModel
from ui.staff.assignStaff import AssignStaffFrame
from ui.staff.addStaff import AddStaffFrame
from ui.staff.editStaff import EditStaffFrame


# ============== Staff Maintenance Page ==============
class StaffMaintenancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_model = EmployeeModel()
        self.create_widgets()
        self.update_summary_metrics()


# ============== Widget Creation ==============
    def create_widgets(self):
        self.configure(fg_color="white")

        # ========== Title ==========
        label = ctk.CTkLabel(self,
                             text="Staff and Maintenance",
                             font=("Arial", 24, "bold"),
                             text_color="black")
        label.pack(pady=(40, 30))

        # ========== Summary Frame ==========
        frame = ctk.CTkFrame(
            self,
            fg_color="#f7f7f7",
            corner_radius=12,
            border_width=1,
            border_color="#e5e7eb",
            height=140
        )
        frame.pack(pady=(10, 20), padx=20, fill="x")
        frame.pack_propagate(False)

        ctk.CTkLabel(frame,
                     text="Summary",
                     font=("Arial", 22, "bold"),
                     text_color="#374151").pack(pady=(20,15), anchor="w", padx=20)


    # ========== Summary Metrics ==========
        horizontal_frame = ctk.CTkFrame(frame, fg_color="#f7f7f7")
        horizontal_frame.pack(pady=10, padx=20, fill="x")

        # Rooms cleaned
        self.cleaned_label = ctk.CTkLabel(horizontal_frame,
                                          text="0",
                                          font=("Arial", 20, "bold"),
                                          text_color="black")
        self.cleaned_label.grid(row=0, column=0, sticky="w", padx=(10, 0))

        cleaned_desc = ctk.CTkLabel(horizontal_frame,
                                    text="rooms cleaned",
                                    font=("Arial", 18, "italic"),
                                    text_color="#6b7280")
        cleaned_desc.grid(row=0, column=1, sticky="w", padx=(10, 100))

        # Rooms dirty
        self.dirty_label = ctk.CTkLabel(horizontal_frame,
                                        text="0",
                                        font=("Arial", 20, "bold"),
                                        text_color="black")
        self.dirty_label.grid(row=0, column=2, sticky="w", padx=(10, 0))

        dirty_desc = ctk.CTkLabel(horizontal_frame,
                                  text="rooms are dirty",
                                  font=("Arial", 18, "italic"),
                                  text_color="#6b7280")
        dirty_desc.grid(row=0, column=3, sticky="w", padx=(10, 100))

        # Staff available
        self.available_label = ctk.CTkLabel(horizontal_frame,
                                            text="0",
                                            font=("Arial", 20, "bold"),
                                            text_color="black")
        self.available_label.grid(row=0, column=4, sticky="w", padx=(10, 0))

        available_desc = ctk.CTkLabel(horizontal_frame,
                                      text="staffs available",
                                      font=("Arial", 18, "italic"),
                                      text_color="#6b7280")
        available_desc.grid(row=0, column=5, sticky="w", padx=(10, 10))


    # ========== Buttons ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        button_frame.pack(pady=(10, 0), padx=(20, 10), fill="x")
        button_frame.pack_propagate(False)

        button_kwargs = dict(font=("Arial", 15, "bold"), width=200, height=40, text_color="white",
                             fg_color="#2563eb", hover_color="#1d4ed8")

        # Assign Staff Button
        assign_btn = ctk.CTkButton(button_frame,
                                   text="Assign Staff",
                                   command=self.assign_staff_popup,
                                   **button_kwargs)
        assign_btn.pack(side="right", padx=(20, 10), pady=10)

        # Add Staff Button
        add_btn = ctk.CTkButton(button_frame,
                                text="Add Staff",
                                command=self.add_staff_popup,
                                **button_kwargs)
        add_btn.pack(side="right", padx=(20, 10), pady=10)

        # Remove Staff Button
        update_btn = ctk.CTkButton(button_frame,
                                   text="Edit Staff",
                                   command=self.edit_staff_popup,
                                   **button_kwargs)
        update_btn.pack(side="right", padx=(20, 10), pady=10)


    # ========== Staff Table ==========
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(pady=(10, 10), padx=(0, 10), fill="both", expand=True)

        columns = ("Staff Name", "Staff ID", "Role", "Assigned to", "Status")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), foreground="#374151")
        style.configure("Treeview", font=("Courier", 11),rowheight=25)
        style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", "#1a1a1a")])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=150)

        self.tree.tag_configure("even_row", background="#f7f7f7")
        self.tree.tag_configure("odd_row", background="#ffffff")

        self.tree.pack(fill="both", expand=True, padx=(20, 10), pady=(0, 10))

        self.populate_staff_list()


# ========== Events ==========

    def update_summary_metrics(self):
        employee_list = self.employee_model.get_all_employees()
        rooms_cleaned = 0
        rooms_dirty = 0
        available_staff = 0

        for employee in employee_list:
            if employee['STATUS'] == 'Available':
                available_staff += 1

        self.cleaned_label.configure(text=str(rooms_cleaned))
        self.dirty_label.configure(text=str(rooms_dirty))
        self.available_label.configure(text=str(available_staff))


    def populate_staff_list(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            employee_data = self.employee_model.get_all_employees()
            for index, employee in enumerate(employee_data):
                full_name = f"{employee['FIRST_NAME']} {employee['LAST_NAME']}"
                tag = "even_row" if index % 2 == 0 else "odd_row"

                self.tree.insert("", "end",
                                 values=(
                                     full_name,
                                     employee["EMPLOYEE_ID"],
                                     employee["POSITION"],
                                     employee["ASSIGNED_TO"],
                                     employee["STATUS"]
                                 ),
                                 tags=(tag,))

            self.update_summary_metrics()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load employee data.\n{str(e)}")


# ========== Staff Popups ==========

    def assign_staff_popup(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("No selection", "Please select a staff member to assign.")
            return

        selected_item = self.tree.item(selected[0])
        staff_id = selected_item["values"][1]  # Assuming Staff ID is the 2nd column

        popup = ctk.CTkToplevel(self)
        popup.title("Assign Staff")
        popup.geometry("400x350")
        popup.grab_set()

        frame = AssignStaffFrame(parent_popup=popup, employee_id=staff_id, parent_page=self)
        frame.pack(fill="both", expand=True)


    def add_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add New Staff")
        popup.geometry("800x800")
        popup.grab_set() # Lock focus to popup

        frame = AddStaffFrame(parent_popup=popup, parent_page=self)
        frame.pack(fill="both", expand=True)


    def edit_staff_popup(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("No selection", "Please select a staff member to update.")
            return

        selected_item = self.tree.item(selected[0])
        staff_id = selected_item["values"][1]  # Assuming Staff ID is the 2nd column

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Staff Details")
        popup.geometry("600x900")
        popup.grab_set()

        frame = EditStaffFrame(parent_popup=popup, employee_id=staff_id, parent_page=self)
        frame.pack(fill="both", expand=True)



# ========== Preview Frame as App ==========
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1400x900")
    root.title("Staff Maintenance Test")

    ctk.set_appearance_mode("light")    # set overall appearance mode: light/dark/system
    ctk.set_default_color_theme("blue") # set default color theme

    page = StaffMaintenancePage(root)
    page.pack(fill="both", expand=True)

    root.mainloop()