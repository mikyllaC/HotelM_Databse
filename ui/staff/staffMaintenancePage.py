# ============== Imports ==============
from tkinter import ttk, messagebox
import customtkinter as ctk

from models.employee import EmployeeModel
from ui.staff.addStaff import AddStaffFrame
from ui.staff.editStaff import EditStaffFrame


# ============== Staff Maintenance Page ==============
class StaffMaintenancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_model = EmployeeModel()
        self.create_widgets()

    # ============== Widget Creation ==============
    def create_widgets(self):
        self.configure(fg_color="#f0f0f0")

        # ========== Title ==========
        label = ctk.CTkLabel(self,
                             text="Staff and Maintenance",
                             font=("Arial", 24, "bold"),
                             text_color="black")
        label.pack(pady=20)

        # ========== Summary Frame ==========
        frame = ctk.CTkFrame(self, fg_color="#c5c4c4", height=120)
        frame.pack(pady=(10, 0), padx=20, fill="x")
        frame.pack_propagate(False)

        ctk.CTkLabel(frame,
                     text="Summary",
                     font=("Arial", 20, "bold"),
                     text_color="black").pack(pady=20, anchor="w", padx=20)

        # ========== Summary Metrics ==========
        horizontal_frame = ctk.CTkFrame(frame, fg_color="#c5c4c4")
        horizontal_frame.pack(pady=10, padx=20, fill="x")

        # Sample summary values (replace with dynamic data later)
        rooms_cleaned = 15
        rooms_dirty = 7
        staffs_available = 5

        # Rooms cleaned
        ctk.CTkLabel(horizontal_frame, text=str(rooms_cleaned),
                     font=("Arial", 18, "bold"), text_color="black").pack(side="left", padx=(0, 5))
        ctk.CTkLabel(horizontal_frame, text="rooms cleaned",
                     font=("Arial", 18, "italic"), text_color="black").pack(side="left", padx=(0, 100))

        # Rooms dirty
        ctk.CTkLabel(horizontal_frame, text=str(rooms_dirty),
                     font=("Arial", 18, "bold"), text_color="black").pack(side="left", padx=(10, 1))
        ctk.CTkLabel(horizontal_frame, text="rooms are dirty",
                     font=("Arial", 18, "italic"), text_color="black").pack(side="left", padx=(5, 100))

        # Staff available
        ctk.CTkLabel(horizontal_frame, text=str(staffs_available),
                     font=("Arial", 18, "bold"), text_color="black").pack(side="left", padx=(100, 1))
        ctk.CTkLabel(horizontal_frame, text="staffs available",
                     font=("Arial", 18, "italic"), text_color="black").pack(side="left", padx=(5, 20))

        # ========== Buttons ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        button_frame.pack(pady=(10, 0), padx=(20, 10), fill="x")
        button_frame.pack_propagate(False)

        # Assign Staff Button
        assign_btn = ctk.CTkButton(button_frame,
                                   text="Assign Staff",
                                   font=("Arial", 15, "bold"),
                                   text_color="white",
                                   width=200,
                                   height=40,
                                   command=self.assign_staff_popup)
        assign_btn.pack(side="right", padx=(20, 10), pady=10)

        # Add Staff Button
        add_btn = ctk.CTkButton(button_frame,
                                text="Add Staff",
                                font=("Arial", 15, "bold"),
                                text_color="white",
                                width=200,
                                height=40,
                                command=self.add_staff_popup)
        add_btn.pack(side="right", padx=(20, 10), pady=10)

        # Remove Staff Button
        update_btn = ctk.CTkButton(button_frame,
                                   text="Edit Staff",
                                   font=("Arial", 15, "bold"),
                                   text_color="white",
                                   width=200,
                                   height=40,
                                   command=self.edit_staff_popup)
        update_btn.pack(side="right", padx=(20, 10), pady=10)

        # ========== Staff Table ==========
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(pady=(10, 10), padx=(0, 10), fill="both", expand=True)

        columns = ("Staff Name", "Staff ID", "Role", "Assigned to", "Status")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Courier", 11))

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=150)

        # # Sample static data
        # sample_data = [
        #     ("Sunday Dimagiba", "000-000-00", "Cleaning", "Floor 12", "Available"),
        #     ("John Doe", "111-111-11", "Maintenance", "Floor 5", "Busy"),
        #     ("Jane Smith", "222-222-22", "Cleaning", "Floor 3", "Available"),
        #     ("Alice Johnson", "333-333-33", "Maintenance", "Floor 8", "Available"),
        #     ("Bob Brown", "444-444-44", "Cleaning", "Floor 10", "Busy"),
        # ]
        # for row in sample_data:
        #     self.tree.insert("", "end", values=row)
        self.populate_staff_list()

        self.tree.tag_configure("highlighted", background="#b3e6ff")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True, padx=(20, 10), pady=(0, 10))

    # ========== Assign Staff Popup ==========
    def assign_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Assign Staff")
        popup.geometry("400x250")
        popup._apply_appearance_mode("light")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Assign Staff to Room", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(popup, text="Staff ID:", font=("Arial", 13)).pack(pady=(5, 0))
        staff_entry = ctk.CTkEntry(popup, width=220)
        staff_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Room/Floor:", font=("Arial", 13)).pack(pady=(10, 0))
        room_options = [f"Floor {i}" for i in range(1, 13)]
        room_var = ctk.StringVar(value=room_options[0])

        try:
            room_dropdown = ctk.CTkComboBox(popup, variable=room_var, values=room_options,
                                            width=220, height=32, font=("Courier", 13))
        except AttributeError:
            room_dropdown = ttk.Combobox(popup, textvariable=room_var, values=room_options,
                                         state="readonly", width=25)
        room_dropdown.pack(pady=5)

        def on_assign():
            staff_id = staff_entry.get()
            room = room_var.get()
            # TODO: Add logic to assign staff here
            print(f"[LOG] Assigned staff {staff_id} to {room}")
            popup.destroy()

        ctk.CTkButton(popup, text="Assign", command=on_assign).pack(pady=(15, 5))
        ctk.CTkButton(popup, text="Cancel", command=popup.destroy, fg_color="gray").pack()


    def populate_staff_list(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            employee_data = self.employee_model.get_all_employees()
            for employee in employee_data:
                # Convert sqlite3.Row to tuple so it shows correctly in the Treeview
                full_name = f"{employee['FIRST_NAME']} {employee['LAST_NAME']}"
                self.tree.insert("", "end", values=(
                    full_name,
                    employee["EMPLOYEE_ID"],
                    employee["POSITION"],
                    employee["ASSIGNED_TO"],
                    employee["STATUS"]
                ))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load employee data.\n{str(e)}")


    def add_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add New Staff")
        popup.geometry("800x800")
        frame = AddStaffFrame(parent=popup)
        frame.pack(fill="both", expand=True)
        popup.grab_set() # used to capture all events (like mouse and keyboard input) to the popup window
        # When you call .grab_set() on a widget (usually a Toplevel), it:
        # Prevents the user from interacting with any other windows in the application
        # until that widget/window is closed or .grab_release() is called.


    def edit_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Staff Details")
        popup.geometry("600x900")
        popup.grab_set()

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a staff member to update.")
            return

        selected_item = self.tree.item(selected[0])
        staff_id = selected_item["values"][1]  # Assuming Staff ID is the 2nd column

        frame = EditStaffFrame(parent_popup=popup, employee_id=staff_id, parent_page=self)
        frame.pack(fill="both", expand=True)



    def on_tree_select(self, event):
        # Clear all tags first
        for item in self.tree.get_children():
            self.tree.item(item, tags=())
        # Highlight selected
        for item in self.tree.selection():
            self.tree.item(item, tags=("highlighted",))


# ========== Preview Frame as App ==========
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Staff Maintenance Test")

    ctk.set_appearance_mode("light")    # set overall appearance mode: light/dark/system
    ctk.set_default_color_theme("blue") # set default color theme

    page = StaffMaintenancePage(root)
    page.pack(fill="both", expand=True)

    root.mainloop()