import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("light")

class GuestListApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Guest List")
        self.geometry("1024x738")

#Placeholder Data 
        guest_data = [
            ["Guest Name", "Contact Information", "Number of Rooms", "Status"],
            ["Sunday", "0916-123-1234", "3", "Checked In"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-"],
        ]

#Title Label
        title_label = ctk.CTkLabel(self, text="Guest Management", 
                                   font=("Arial", 28, "bold"))
        title_label.pack(side="top", 
                         anchor="n", 
                         pady=(35, 45), 
                         padx=(10, 0))
        


#Guest Information
        self.right_frame = ctk.CTkFrame(self, width=250, 
                        height=738, 
                        corner_radius=10, 
                        border_width=1,)
        self.right_frame.configure(border_width=1, 
                       corner_radius=10)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack_forget()  # Hide the frame initially

        right_label = ctk.CTkLabel(self.right_frame, text="Guest Information", 
                       font=("Arial", 18, "bold"))
        right_label.pack(pady=10)

        # Function to update right_frame with guest info
        def show_guest_info(guest_info):
            # Remove previous widgets except the title and close button
            for widget in self.right_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Guest Information":
                    continue
                if isinstance(widget, ctk.CTkButton):
                    continue
                widget.destroy()

            # Display guest info 
            labels = guest_data[0]
            extra_info = {
                "Email": "sunday@example.com",
                "Pax": "5",
                "Address": "123 Main St, City",
                "Check-in Date": "2023-10-01",
                "Special Requests": "Late check-in, Vegan meals",
                "Room Type": "Deluxe Suite",
                "Payment Status": "Paid",
                
            }
            wraplength = 200  # Adjust as needed for your frame width

            for i, value in enumerate(guest_info):
                info_label = ctk.CTkLabel(
                    self.right_frame,
                    text=f"{labels[i]}: {value}",
                    font=("Arial", 14),
                    wraplength=wraplength,
                    justify="left"
                )
                info_label.pack(anchor="w", padx=20, pady=2, fill="x")

            # Add extra info fields
            for key, value in extra_info.items():
                extra_label = ctk.CTkLabel(
                    self.right_frame,
                    text=f"{key}: {value}",
                    font=("Arial", 14),
                    wraplength=wraplength,
                    justify="left"
                )
                extra_label.pack(anchor="w", padx=20, pady=2, fill="x")

        # Modify the row selection handler to show/hide the right frame and guest info
        def on_row_select(event):
            selected_item = self.treeview.selection()
            if selected_item:
                item_values = self.treeview.item(selected_item[0], "values")
                if item_values and item_values[0] != "-":
                    self.right_frame.pack(side = "left", padx=(1, 20), pady=20)
                    show_guest_info(item_values)
                else:
                    self.right_frame.pack_forget()
            else:
                self.right_frame.pack_forget()

        # Close button to the right_frame
        def close_right_frame():
            self.right_frame.pack_forget()

        close_button = ctk.CTkButton(
            self.right_frame,
            text="X",
            command=close_right_frame,
            width=20,
            height=20,
            border_width=0,
            corner_radius=10
        )
        close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

    #Update Payment
        EditUpdate_button = ctk.CTkButton(
            self.right_frame, 
            text="Update Payment",
            font=("Arial", 16, "bold"),
            width=180,
            height=40
        )
        EditUpdate_button.pack(
            side="bottom",
            padx=20, 
            pady=10, 
            anchor="n")
        edit_guest_button = ctk.CTkButton(
                self.right_frame,
                text="Edit Guest Info",
                font=("Arial", 16, "bold"),
                width=180,
                height=40
            )
        edit_guest_button.pack(
                side="bottom",
                padx=20,
                pady=(0, 10),
                anchor="n"
            )
        
        # Search and Filter Frame (below the Guest Management Title)
        self.search_filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_filter_frame.pack(side="top", 
                                      anchor="w", 
                                      padx=(35, 0), 
                                      pady=(0, 0))

            # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
                self.search_filter_frame,
                width=220,
                height=36,
                placeholder_text="Search guest name...",
                textvariable=self.search_var,
                font=("Arial", 14)
            )
        self.search_entry.pack(side="left", padx=(0, 10))


    #Function that update payment pops another window
        def update_payment():
            payment_window = ctk.CTkToplevel(self)
            payment_window.title("Update Payment")
            payment_window.geometry("400x300")
            title_label = ctk.CTkLabel(payment_window, 
                                       text="Update Payment",
                                       font=("Arial", 20, "bold"))
            title_label.pack(pady=(20, 10))
            
            # Add content to the payment window
            label = ctk.CTkLabel(payment_window, 
                                 text="Enter new payment status:", 
                                 font=("Arial", 14))
            label.pack(pady=(30, 10))

            payment_status_var = tk.StringVar(value="Paid")
            payment_status_combobox = ctk.CTkComboBox(
                payment_window,
                values=["Paid", 
                        "Unpaid", 
                        "Pending", 
                        "Refunded"],
                variable=payment_status_var,
                width=200
            )
            payment_status_combobox.pack(pady=10)

            def save_payment():
                # Here you would update the payment status in your data source
                # For now, just close the window
                payment_window.destroy()

            save_button = ctk.CTkButton(payment_window, 
                                        text="Update", 
                                        command=save_payment, 
                                        width=120)
            save_button.pack(pady=20)

        # Connect the Update Payment button to open the update payment window
        EditUpdate_button.configure(command=update_payment)

            # Filter Combobox
        self.filter_var = tk.StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
                self.search_filter_frame,
                width=160,
                height=36,
                values=["All Status", "Checked In", "Checked Out", "Reserved"],
                variable=self.filter_var,
                font=("Arial", 14)
            )
        self.filter_combobox.pack(side="left", padx=(0, 10))

            # Search Button
        def filter_table(*args):
                search_text = self.search_var.get().lower()
                selected_status = self.filter_var.get()
                # Clear table
                for item in self.treeview.get_children():
                    self.treeview.delete(item)
                # Filter and insert rows
                for row in guest_data[1:]:
                    name, _, _, status = row
                if (search_text in name.lower() or not search_text) and \
                   (selected_status == "All Status" or status == selected_status):
                    self.treeview.insert("", "end", values=row)

        self.search_entry.bind("<KeyRelease>", lambda e: filter_table())
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: filter_table())

        # Add "Create Reservation" button beside the search and filter bar
        create_reservation_button = ctk.CTkButton(
            self.search_filter_frame,
            text="Create Reservation",
            font=("Arial", 16, "bold"),
            width=180,
            height=36
        )
        # Add "Create Reservation" button to the left of the search/filter bar
        create_reservation_button.pack(side="left", padx=(0, 10))

        # Add random text aligned to the right of the search/filter frame
        random_text_label = ctk.CTkLabel(
            self.search_filter_frame,
            text="'Let the pain teach you how to dougie'",
            font=("Arial", 12, "italic", "bold"),
            text_color="#888888"
        )
        random_text_label.pack(side="right", padx=75)

# Guest List
        self.left_frame = ctk.CTkFrame(self, 
               width=750, 
               height=738, 
               corner_radius=10, 
               border_width=0, 
               fg_color="transparent")
        self.left_frame.pack_propagate(False)
        # Align left_frame at the top, filling vertically
        self.left_frame.pack(side="left", padx=(10, 1), pady=(15, 10), fill="y", anchor="n")

    # Add table
        style = tk.ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 15, "bold"), 
                pad=(10, 0),
                anchor="w")  # Left align headings
        style.configure("Treeview", rowheight=30, 
                font=("Courier", 14), 
                anchor="w")  # Left align cells

        self.treeview = tk.ttk.Treeview(self.left_frame, 
            columns=guest_data[0], 
            show="headings", 
            height=20)
        self.treeview.pack(expand=True, fill="both", padx=10, pady=20)
        for col in guest_data[0]:
            self.treeview.heading(col, text=col, anchor="w")  # Left align heading text
            self.treeview.column(col, width=200, anchor="w")  # Left align column content
        for row in guest_data[1:]:
            self.treeview.insert("", "end", values=row)

        # Bind the selection event to the Treeview (after self.treeview is created)
        self.treeview.bind("<<TreeviewSelect>>", on_row_select)

        # Add a scrollbar to the Treeview
        scrollbar = tk.ttk.Scrollbar(self.left_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

#Display output can be deleted upon merging
if __name__ == "__main__":
    app = GuestListApp()
    app.mainloop()