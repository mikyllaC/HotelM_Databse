import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
#For image handling
from PIL import Image, ImageTk
from tkinter import filedialog

#------------Notes-----------
#Need to fix image, image not appearing in right frame
#Added pop ups for edit room and delete room (Delete room is located in the edit room pop up)
#For photo testing if fixing it, added placeholder image on asset folder

ctk.set_appearance_mode("light")

class RoomManagementPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master.geometry("1600x800")
        self.configure(fg_color="#e0e0e0")
        
        #Placeholder Data
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
            "Image": "assets/placeholder.jpeg",
            "Description": "lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Room Number": "001",
            "Room Floor": "3rd Floor",
            "Room Size": "100sqm",
            "Room Type and Capacity": "Deluxe Suite, 2 Beds, 2-4 Pax",
            "Amenities": "Wifi, Refrigrator, TV, Aircon, Bathtub",
            "Status": "Available",
                  }

        wraplength = 450

#Still fixing how am I gonna insert image - Sofia
        for i, value in enumerate(room_info):
            info_label = ctk.CTkLabel(self.right_frame, text=f"{labels[i]}: {value}", font=("Arial", 14),
                                      wraplength=wraplength, justify="left")
            info_label.pack(anchor="w", padx=20, pady=2)
            if i == 0 and extra_info["Image"]:
                try:
                    img = Image.open(extra_info["placeholder.jpeg"])
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img = img.resize((120, 120))
                    photo = ImageTk.PhotoImage(img)
                    if not hasattr(self, 'room_images'):
                        self.room_images = []
                    self.room_images.append(photo)  # Keep reference to avoid garbage collection
                    img_label = ctk.CTkLabel(self.right_frame, image=photo, text="")
                    img_label.image = photo  # Keep reference for the label
                    img_label.pack(anchor="w", padx=20, pady=5)
                except Exception as e:
                    pass

        for key, value in extra_info.items():
            extra_label = ctk.CTkLabel(self.right_frame, text=f"{key}: {value}", font=("Arial", 14),
                                       wraplength=wraplength, justify="left")
            extra_label.pack(anchor="w", padx=20, pady=2)

    def build_search_filter_bar(self):
        self.search_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_filter_frame.pack(side="top", anchor="w", padx=(35, 0))

        # Create Room Button
        create_room_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Create Room",
            font=("Arial", 16, "bold"),
            width=180,
            height=36,
            command=self.create_room_popup
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

        # Room Number and Room Floor side by side
        room_num_floor_frame = ctk.CTkFrame(editRoom_window, fg_color="transparent")
        room_num_floor_frame.pack(anchor="w", padx=40, pady=(10, 0), fill="x")

        ctk.CTkLabel(room_num_floor_frame, text="Room Number:", font=("Arial", 14)).pack(side="left")
        room_number_entry = ctk.CTkEntry(room_num_floor_frame, width=140)
        room_number_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(room_num_floor_frame, text="Room Floor:", font=("Arial", 14)).pack(side="left")
        room_floor_entry = ctk.CTkEntry(room_num_floor_frame, width=140)
        room_floor_entry.pack(side="left", padx=(5, 0))

                # Room Size
        # Room Size and Room Type/Capacity side by side
        size_type_frame = ctk.CTkFrame(editRoom_window, fg_color="transparent")
        size_type_frame.pack(anchor="w", padx=40, pady=(10, 0), fill="x")

        ctk.CTkLabel(size_type_frame, text="Room Size:", font=("Arial", 14)).pack(side="left")
        room_size_entry = ctk.CTkEntry(size_type_frame, width=140)
        room_size_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(size_type_frame, text="Room Type and Capacity:", font=("Arial", 14)).pack(side="left")
        room_type_entry = ctk.CTkEntry(size_type_frame, width=140)
        room_type_entry.pack(side="left", padx=(5, 0))

                # Amenities
        ctk.CTkLabel(editRoom_window, text="Amenities:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        amenities_entry = ctk.CTkEntry(editRoom_window, width=300)
        amenities_entry.pack(anchor="w", padx=40, pady=2)
                # Status
        ctk.CTkLabel(editRoom_window, text="Status:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        status_combobox = ctk.CTkComboBox(editRoom_window, values=["Available", "Occupied", "Reserved", "Under Maintenance"], width=300)
        status_combobox.pack(anchor="w", padx=40, pady=2)

                # Description
        ctk.CTkLabel(editRoom_window, text="Description:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        description_entry = ctk.CTkTextbox(editRoom_window, width=600, height=80)
        description_entry.pack(anchor="w", padx=40, pady=2)


        def save_edit():
            editRoom_window.destroy()

        button_frame = ctk.CTkFrame(editRoom_window, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Save",
            font=("Arial", 16, "bold"),
            command=save_edit,
            width=120,
            height=40,
            fg_color="#4caf50",  # Green color
            hover_color="#388e3c"  # Darker green on hover
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            button_frame,
            text="Delete Room",
            font=("Arial", 16, "bold"),
            width=120,
            height=40,
            fg_color="#e57373",  # Red color
            hover_color="#c62828"  # Darker red on hover
        ).pack(side="left", padx=10)


#Create Room Function
    def create_room_popup(self):
        createRoom_window = ctk.CTkToplevel(self)
        createRoom_window.title("Create Room")
        createRoom_window.geometry("1200x750")

        ctk.CTkLabel(createRoom_window, text="Create Room", font=("Arial", 20, "bold")).pack(pady=(20, 10))

        # Room Number and Room Floor side by side
        room_num_floor_frame = ctk.CTkFrame(createRoom_window, fg_color="transparent")
        room_num_floor_frame.pack(anchor="w", padx=40, pady=(10, 0), fill="x")

        ctk.CTkLabel(room_num_floor_frame, text="Room Number:", font=("Arial", 14)).pack(side="left")
        room_number_entry = ctk.CTkEntry(room_num_floor_frame, width=140)
        room_number_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(room_num_floor_frame, text="Room Floor:", font=("Arial", 14)).pack(side="left")
        room_floor_entry = ctk.CTkEntry(room_num_floor_frame, width=140)
        room_floor_entry.pack(side="left", padx=(5, 0))

        # Room Size and Room Type/Capacity side by side
        size_type_frame = ctk.CTkFrame(createRoom_window, fg_color="transparent")
        size_type_frame.pack(anchor="w", padx=40, pady=(10, 0), fill="x")

        ctk.CTkLabel(size_type_frame, text="Room Size:", font=("Arial", 14)).pack(side="left")
        room_size_entry = ctk.CTkEntry(size_type_frame, width=140)
        room_size_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(size_type_frame, text="Room Type and Capacity:", font=("Arial", 14)).pack(side="left")
        room_type_entry = ctk.CTkEntry(size_type_frame, width=140)
        room_type_entry.pack(side="left", padx=(5, 0))

        # Amenities
        ctk.CTkLabel(createRoom_window, text="Amenities:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        amenities_entry = ctk.CTkEntry(createRoom_window, width=300)
        amenities_entry.pack(anchor="w", padx=40, pady=2)

        # Status
        ctk.CTkLabel(createRoom_window, text="Status:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        status_combobox = ctk.CTkComboBox(createRoom_window, values=["Available", "Occupied", "Reserved", "Under Maintenance"], width=300)
        status_combobox.pack(anchor="w", padx=40, pady=2)

        # Description
        ctk.CTkLabel(createRoom_window, text="Description:", font=("Arial", 14)).pack(anchor="w", padx=40, pady=(10, 0))
        description_entry = ctk.CTkTextbox(createRoom_window, width=600, height=80)
        description_entry.pack(anchor="w", padx=40, pady=2)

        # Placeholder for image upload
        # Image Upload Section
        image_frame = ctk.CTkFrame(createRoom_window, fg_color="transparent")
        image_frame.pack(anchor="w", padx=40, pady=(10, 0))

        image_label = ctk.CTkLabel(image_frame, text="Room Image:", font=("Arial", 14))
        image_label.pack(side="left")

        uploaded_image = [None]  # Use list to allow modification in nested function

        def upload_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
            )
            if file_path:
                try:
                    img = Image.open(file_path)
                    img.thumbnail((120, 120))
                    photo = ImageTk.PhotoImage(img)
                    uploaded_image[0] = photo  # Keep reference to avoid garbage collection
                    preview_label.configure(image=photo, text="")
                    preview_label.image = photo
                except Exception as e:
                    preview_label.configure(text="Failed to load image", image=None)

        upload_btn = ctk.CTkButton(
            image_frame,
            text="Upload Image",
            font=("Arial", 14, "bold"),
            command=upload_image,
            width=120,
            height=40
        )
        upload_btn.pack(side="left", padx=(10, 0))

        preview_label = ctk.CTkLabel(createRoom_window, text="No image selected", width=120, height=120)
        preview_label.pack(anchor="w", padx=40, pady=(5, 0))

        def save_create():
            createRoom_window.destroy()

        button_frame = ctk.CTkFrame(createRoom_window, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Create",
            font=("Arial", 16, "bold"),
            command=save_create,
            width=120,
            height=40,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(side="left", padx=10)

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
    root.title("Room Management")
    app.pack(fill="both",
             expand=True)
    root.mainloop()