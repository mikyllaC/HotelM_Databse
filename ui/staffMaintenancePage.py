import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class HouseKeepingListWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Housekeeping and Maintenance")
        self.geometry("1024x738")
        self.configure(bg="#f0f0f0")

    #Title Label
        label = ctk.CTkLabel(self, 
                             text="Staff and Maintenance", 
                             font=("Arial", 24, "bold")
                             , text_color="black",)
        label.pack(pady=20)

    #Summary Frame
        frame = ctk.CTkFrame(self, fg_color="#c5c4c4")
        frame.pack(pady=(10, 0),
               padx=20,
               fill="x",
               expand=False)
        frame.configure(height=120)
        frame.pack_propagate(False)

    # Add a sample text label inside the frame
        sample_label = ctk.CTkLabel(frame, 
                                    text="Summary", 
                                    font=("Arial", 20, "bold"), 
                                    text_color="black")
        sample_label.pack(pady=20, anchor="w", padx=20)

    # Create a frame to hold the horizontal texts
        horizontal_frame = ctk.CTkFrame(frame, fg_color="#c5c4c4")
        horizontal_frame.pack(pady=10, padx=20, fill="x")

    #Data stuff Place holder only
        # Example data
        rooms_cleaned = 15
        rooms_dirty = 7
        staffs_available = 5

    # Number and label for rooms cleaned, dirty, and staffs available
        #Rooms Cleaned
        num_label1 = ctk.CTkLabel(horizontal_frame, 
                                  text=str(rooms_cleaned), 
                                  font=("Arial", 18, "bold"), 
                                  text_color="black")
        num_label1.pack(side="left", padx=(0, 5))

        label1 = ctk.CTkLabel(horizontal_frame, 
                              text="rooms cleaned", 
                              font=("Arial", 18, "italic"), 
                              text_color="black")
        label1.pack(side="left", padx=(0, 100))

    #Rooms Dirty 
        num_label2 = ctk.CTkLabel(horizontal_frame, 
                                  text=str(rooms_dirty), 
                                  font=("Arial", 18, "bold"), 
                                  text_color="black")
        num_label2.pack(side="left", padx=(10, 1))

        label2 = ctk.CTkLabel(horizontal_frame, 
                              text="rooms are dirty", 
                              font=("Arial", 18, "italic"), 
                              text_color="black")
        label2.pack(side="left", padx=(5, 100))

    #Staffs Available
        num_label3 = ctk.CTkLabel(horizontal_frame, 
                                  text=str(staffs_available), 
                                  font=("Arial", 18, "bold"), 
                                  text_color="black")
        num_label3.pack(side="left", padx=(100, 1))

        label3 = ctk.CTkLabel(horizontal_frame, 
                              text="staffs available", 
                              font=("Arial", 18, "italic"), 
                              text_color="black")
        label3.pack(side="left",padx=(5, 20))

    #Buttons Frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(10, 0),
                          padx=(20, 10),
                          fill="x",
                          expand=False)
        button_frame.configure(height=70)
        button_frame.pack_propagate(False)

    #3 Buttons 
        #Assign Staff
        button1 = ctk.CTkButton(button_frame,
                                text="Assign Staff",
                                font=("Arial", 15, "bold"),
                                text_color="white",
                                width=200,
                                height=40)
        button1.pack(side="right", padx=(20, 10), pady=10)

        def assign_staff_popup():
            popup = ctk.CTkToplevel(self)
            popup.title("Assign Staff")
            popup.geometry("400x250")
            label = ctk.CTkLabel(popup, text="Assign Staff to Room", font=("Arial", 16, "bold"))
            label.pack(pady=(20, 10))
            popup._apply_appearance_mode("light")

            staff_label = ctk.CTkLabel(popup, text="Staff ID:", font=("Arial", 13))
            staff_label.pack(pady=(5, 0))
            staff_entry = ctk.CTkEntry(popup, width=220)
            staff_entry.pack(pady=5)
            popup._apply_appearance_mode("light")

           #dropdown
            room_label = ctk.CTkLabel(popup, text="Room/Floor:", 
                                      font=("Arial", 13))
            room_label.pack(pady=(10, 0)) 
            
            room_options = ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", "Floor 7", "Floor 8", "Floor 9", "Floor 10", "Floor 11", "Floor 12"]
            room_var = tk.StringVar(value=room_options[0])
            try:
                room_dropdown = ctk.CTkComboBox(
                    popup,
                    variable=room_var,
                    values=room_options,
                    width=220,
                    height=32,
                    font=("Courier", 13)
                )
                room_dropdown.pack(pady=5, padx=(10,20))
                room_dropdown.pack(pady=5)
            except AttributeError:
                # fallback if CTkComboBox is not available
                room_dropdown = ttk.Combobox(popup, textvariable=room_var, values=room_options, state="readonly", width=25)
                room_dropdown.pack(pady=5)

            # Example list of rooms/floors
            room_options = ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", "Floor 7", "Floor 8", "Floor 9", "Floor 10", "Floor 11", "Floor 12"]
            room_var = tk.StringVar(value=room_options[0])
            room_dropdown = ttk.Combobox(popup, textvariable=room_var, values=room_options, state="readonly", width=25)
            room_dropdown.pack(pady=5)
            popup._apply_appearance_mode("light")

        #Add logic here to assign staff to room
            def on_assign():
                staff_id = staff_entry.get()
                #room = room_entry.get()
                # Add logic to assign staff here
                popup.destroy()

            assign_btn = ctk.CTkButton(popup, text="Assign", command=on_assign)
            assign_btn.pack(pady=(15, 5))
            cancel_btn = ctk.CTkButton(popup, text="Cancel", command=popup.destroy, fg_color="gray")
            cancel_btn.pack()
            popup._apply_appearance_mode("light")

        button1.configure(command=assign_staff_popup)

        #Add Staff
        button2 = ctk.CTkButton(button_frame,
                                text="Add Staff",
                                font=("Arial", 15, "bold"),
                                text_color="white",
                                width=200,
                                height=40)
        button2.pack(side="right", padx=(20, 10), pady=10)

        #Remove Staff
        button3 = ctk.CTkButton(button_frame,
                                text="Remove Staff",
                                font=("Arial", 15, "bold"),
                                text_color="white",
                                width=200,
                                height=40)
        button3.pack(side="right", padx=(20, 10), pady=10)

        def remove_staff_popup(): 
            popup = ctk.CTkToplevel(self)
            popup.title("Remove Staff")
            popup.geometry("350x180")
            label = ctk.CTkLabel(popup, text="Enter Staff ID to remove:", font=("Arial", 14))
            label.pack(pady=(20, 10))
            entry = ctk.CTkEntry(popup, width=200)
            entry.pack(pady=5)
            def on_remove():
                staff_id = entry.get()

                # You can add logic here to remove staff from the table
                popup.destroy()
            remove_btn = ctk.CTkButton(popup, text="Remove", command=on_remove)
            remove_btn.pack(pady=(15, 5))
            cancel_btn = ctk.CTkButton(popup, text="Cancel", command=popup.destroy, fg_color="gray")
            cancel_btn.pack() 
            # Set popup to light mode
            popup._apply_appearance_mode("light")

        button3.configure(command=remove_staff_popup)

    #table frame
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(pady=(10, 10), 
                         padx=(0,10), 
                         fill="both", 
                         expand=True)

        # Create a Treeview widget for the table
        columns = ("Staff Name", "Staff ID", "Role", "Assigned to", "Status")

        # Define a style for headings
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        tree = ttk.Treeview(table_frame, 
                            columns=columns, 
                            show="headings", 
                            height=20)

        # Define headings
        for col in columns:
            tree.heading(col,  
                         text=col, 
                         anchor="w")
            tree.column(col, 
                        anchor="w", 
                        width=150)
            tree.column(col, 
                        anchor="w", 
                        width=150)

        # Placeholder Data
        sample_data = [
            ("Sunday Dimagiba", "000-000-00", "Cleaning", "Floor 12", "Available"),
            ("John Doe", "111-111-11", "Maintenance", "Floor 5", "Busy"),
            ("Jane Smith", "222-222-22", "Cleaning", "Floor 3", "Available"),
            ("Alice Johnson", "333-333-33", "Maintenance", "Floor 8", "Available"),
            ("Bob Brown", "444-444-44", "Cleaning", "Floor 10", "Busy"),
        ]

        # Insert sample data into the table
        for row in sample_data:
            tree.insert("", "end", values=row)


        style.configure("Treeview", font=("Courier", 11))
        tree.pack(fill="both", expand=True, padx=(20,10), pady=(0, 10))

        # Highlight row on selection
        tree.tag_configure("highlighted", background="#b3e6ff")

        def on_tree_select(event):
            # Remove highlight from all rows
            for item in tree.get_children():
                tree.item(item, tags=())
            # Highlight all selected rows
            for item in tree.selection():
                tree.item(item, tags=("highlighted",))

        tree.bind("<<TreeviewSelect>>", on_tree_select)

       
#temp display of output
if __name__ == "__main__":
    app = HouseKeepingListWindow()
    app.mainloop()