# ============== Imports ==============
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


# ============== Staff Maintenance Page ==============
class StaffMaintenancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
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

        # Add Staff Button (to be implemented later)
        add_btn = ctk.CTkButton(button_frame,
                                text="Add Staff",
                                font=("Arial", 15, "bold"),
                                text_color="white",
                                width=200,
                                height=40)
        add_btn.pack(side="right", padx=(20, 10), pady=10)

        # Remove Staff Button
        remove_btn = ctk.CTkButton(button_frame,
                                   text="Remove Staff",
                                   font=("Arial", 15, "bold"),
                                   text_color="white",
                                   width=200,
                                   height=40,
                                   command=self.remove_staff_popup)
        remove_btn.pack(side="right", padx=(20, 10), pady=10)

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

        # Sample static data
        sample_data = [
            ("Sunday Dimagiba", "000-000-00", "Cleaning", "Floor 12", "Available"),
            ("John Doe", "111-111-11", "Maintenance", "Floor 5", "Busy"),
            ("Jane Smith", "222-222-22", "Cleaning", "Floor 3", "Available"),
            ("Alice Johnson", "333-333-33", "Maintenance", "Floor 8", "Available"),
            ("Bob Brown", "444-444-44", "Cleaning", "Floor 10", "Busy"),
        ]
        for row in sample_data:
            self.tree.insert("", "end", values=row)

        self.tree.tag_configure("highlighted", background="#b3e6ff")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True, padx=(20, 10), pady=(0, 10))

    # ========== Assign Staff Popup ==========
    def assign_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Assign Staff")
        popup.geometry("400x250")
        popup._apply_appearance_mode("light")

        ctk.CTkLabel(popup, text="Assign Staff to Room", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(popup, text="Staff ID:", font=("Arial", 13)).pack(pady=(5, 0))
        staff_entry = ctk.CTkEntry(popup, width=220)
        staff_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Room/Floor:", font=("Arial", 13)).pack(pady=(10, 0))
        room_options = [f"Floor {i}" for i in range(1, 13)]
        room_var = tk.StringVar(value=room_options[0])

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

    # ========== Remove Staff Popup ==========
    def remove_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Remove Staff")
        popup.geometry("350x180")
        popup._apply_appearance_mode("light")

        ctk.CTkLabel(popup, text="Enter Staff ID to remove:", font=("Arial", 14)).pack(pady=(20, 10))
        entry = ctk.CTkEntry(popup, width=200)
        entry.pack(pady=5)

        def on_remove():
            staff_id = entry.get()
            # TODO: Add logic to remove staff from the table
            print(f"[LOG] Removed staff with ID {staff_id}")
            popup.destroy()

        ctk.CTkButton(popup, text="Remove", command=on_remove).pack(pady=(15, 5))
        ctk.CTkButton(popup, text="Cancel", command=popup.destroy, fg_color="gray").pack()

    # ========== Table Row Selection Handler ==========
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
    page = StaffMaintenancePage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()