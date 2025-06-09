import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

ctk.set_appearance_mode("light")

class RoomManagementPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master.geometry("1600x800")
        self.configure(fg_color="#e0e0e0")
        self.room_data = [
            ["Room No.", "Room Type", "Price", "Status"],
            ["001", "Standard", "P5,000", "Available"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
        ]
        self.guest_data = self.room_data  # Use room_data for guest_data to avoid attribute errors
        self.build_ui()

    def build_title_label(self):
        title_label = ctk.CTkLabel(self, text="Room Management", font=("Arial", 28, "bold"))
        title_label.pack(side="top", anchor="n", pady=(35, 45), padx=(10, 0))

    def build_ui(self):
        self.build_title_label()
        self.build_right_frame()
        self.build_search_filter_bar()
        self.build_left_table()

    #Room Information Frame
    def build_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, width=900, height=738, corner_radius=10, border_width=1)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack_forget()

        #Label for Room Information Frame
        right_label = ctk.CTkLabel(self.right_frame, text="Room Information", font=("Arial", 18, "bold"))
        right_label.pack(pady=10)

        close_button = ctk.CTkButton(
            self.right_frame,
            text="X",
            command=self.close_right_frame,
            width=20,
            height=20,
            corner_radius=10
            , fg_color="#e57373", hover_color="#c62828"
        )
        close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

        #Buttons on right frame
        self.EditRoom = ctk.CTkButton(
            self.right_frame,
            text="Edit Room",
            font=("Arial", 16, "bold"),
            width=180,
            height=40,
            command=self.edit_room_popup
        )
        self.EditRoom.pack(side="bottom", padx=20, pady=10)

    #Close right frame function
    def close_right_frame(self):
        self.right_frame.pack_forget()

    def show_room_info(self, room_info):
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Room Information":
                continue
            if isinstance(widget, ctk.CTkButton):
                continue
            widget.destroy()
        # Display guest information (placeholder data)
        labels = self.room_data[0]
        extra_info = {
            "Email": "sunday@example.com",
            "Pax": "5",
            "Address": "123 Main St, City",
            "Check-in Date": "2023-10-01",
            "Special Requests": "Late check-in, Vegan meals",
            "Room Type": "Deluxe Suite",
            "Payment Status": "Paid",
        }

        wraplength = 200

        for i, value in enumerate(room_info):
            info_label = ctk.CTkLabel(self.right_frame, text=f"{labels[i]}: {value}", font=("Arial", 14),
                                      wraplength=wraplength, justify="left")
            info_label.pack(anchor="w", padx=20, pady=2, fill="x")

        for key, value in extra_info.items():
            extra_label = ctk.CTkLabel(self.right_frame, text=f"{key}: {value}", font=("Arial", 14),
                                       wraplength=wraplength, justify="left")
            extra_label.pack(anchor="w", padx=20, pady=2, fill="x")

    def build_search_filter_bar(self):
        self.search_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_filter_frame.pack(side="top", anchor="w", padx=(35, 0), expand=True, fill="x")

        # Create Room Button
        create_room_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Create Room",
            font=("Arial", 16, "bold"),
            width=180,
            height=36
        )
        create_room_button.pack(side="left", padx=(0, 10))
        
        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.search_filter_frame,
            width=220,
            height=36,
            placeholder_text="Search room...",
            textvariable=self.search_var,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = tk.StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.search_filter_frame,
            width=160,
            height=36,
            values=["Available", "Occupied", "Reserved", "Available", "Under Maintance"],
            variable=self.filter_var,
            font=("Arial", 14)
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        # Search/Filter Event Binding
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table())
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.filter_table())

        self.search_entry.bind("<KeyRelease>", lambda _: self.filter_table())
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda _: self.filter_table())


    def filter_table(self):
        search_text = self.search_var.get().lower()
        selected_status = self.filter_var.get()

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for row in self.guest_data[1:]:
            name, _, _, status = row
            if (search_text in name.lower() or not search_text) and \
               (selected_status == "All Status" or status == selected_status):
                self.treeview.insert("", "end", values=row)

    #Edit Room Function
    def edit_room_popup(self):
        editRoom_window = ctk.CTkToplevel(self)
        editRoom_window.title("Edit Room")
        editRoom_window.geometry("1200x600")

        ctk.CTkLabel(editRoom_window, text="Edit Room", font=("Arial", 20, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(editRoom_window, text="lorem ipsum", font=("Arial", 14)).pack(pady=(30, 10))


        def save_edit():
            editRoom_window.destroy()

        ctk.CTkButton(editRoom_window, text="Save", font=("Arial", 16, "bold"), command=save_edit, width=120).pack(pady=20)
        ctk.CTkButton(editRoom_window, text="Delete Room", font=("Arial", 16, "bold"), width=120).pack(pady=20)

    #Function for table
    def build_left_table(self):
        self.left_frame = ctk.CTkFrame(self, width=1000, height=738, corner_radius=10,
                                       border_width=0, fg_color="transparent")
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side="left", padx=(10, 1), pady=(15, 10), anchor="n")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 15, "bold"), anchor="w")
        style.configure("Treeview", rowheight=30, font=("Courier", 14), anchor="w")
        style.configure("Treeview", rowheight=30, font=("Courier", 14), anchor="w")

        self.treeview = ttk.Treeview(self.left_frame, columns=self.guest_data[0], show="headings", height=20)
        self.treeview.pack(expand=True, fill="both", padx=10, pady=20)

        for col in self.guest_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, width=200, anchor="w")

        for row in self.guest_data[1:]:
            self.treeview.insert("", "end", values=row)

        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

    #Function to handle row selection in the table
    def on_row_select(self, _):
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item[0], "values")
            if item_values and item_values[0] != "-":
                self.right_frame.pack(side="left", padx=(1, 20), pady=20)
                self.show_room_info(item_values)
            else:
                self.right_frame.pack_forget()
        else:
            self.right_frame.pack_forget()


#Temp run
if __name__ == "__main__":
    root = ctk.CTk()
    app = RoomManagementPage(root)
    app.pack(fill="both",
             expand=True)
    root.mainloop()
