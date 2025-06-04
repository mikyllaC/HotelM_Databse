import customtkinter as ctk


class AddStaffFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="white")
        self.create_widgets()

    def create_widgets(self):
        # ========== Header ==========
        header = ctk.CTkLabel(self, text="Add New Staff", font=("Arial", 24, "bold"), text_color="black")
        header.pack(pady=(30, 20))

        # ========== Form Frame ==========
        form_frame = ctk.CTkFrame(self, fg_color="#f4f4f4")
        form_frame.pack(padx=40, pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure((0, 1), weight=1)  # Make both columns expand equally

        # Form Fields
        fields = [
            ("First Name", "entry_first_name"),
            ("Last Name", "entry_last_name"),
            ("Staff ID", "entry_id"),
            ("Email", "entry_email"),
            ("Phone", "entry_phone"),
            ("Role", "entry_role"),
        ]
        self.entries = {}

        for i, (label_text, var_name) in enumerate(fields):
            label = ctk.CTkLabel(form_frame, text=label_text + ":", font=("Arial", 14), text_color="black")
            label.grid(row=i, column=0, sticky="e", padx=(20, 10), pady=10)

            entry = ctk.CTkEntry(form_frame, width=300, height=35)
            entry.grid(row=i, column=1, sticky="w", padx=(0, 20), pady=10)

            self.entries[var_name] = entry

        # ========== Buttons ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 30))

        ctk.CTkButton(button_frame, text="Save", width=140, command=self.save_staff).pack(side="left", padx=20)
        ctk.CTkButton(button_frame, text="Cancel", width=140, fg_color="gray", command=self.master.destroy).pack(side="left", padx=20)

    def save_staff(self):
        staff_data = {label: entry.get() for label, entry in self.entries.items()}
        print("[LOG] New staff data saved:", staff_data)
        self.master.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Add Staff")
    root.geometry("1600x900")
    frame = AddStaffFrame(master=root)
    frame.pack(fill="both", expand=True)
    root.configure(bg="#f0f0f0")
    root.mainloop()