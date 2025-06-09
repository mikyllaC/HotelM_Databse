import customtkinter as ctk


class CreateReservation(ctk.CTkFrame):
    def __init__(self, parent, guest_info=None):
        super().__init__(parent)
        self.master.title("Create Reservation")
        self.master.geometry("1600x800")
        self.configure(fg_color="white")

        #List
        self.label = ctk.CTkLabel(self, 
                                  text="Create a New Reservation", 
                                  font=("Arial", 25, "bold"))
        self.label.pack(pady=20)

        self.list_frame = ctk.CTkFrame(self, 
                                       fg_color="transparent", 
                                       width=500, 
                                       height=400)
        self.list_frame.pack(anchor = "sw", 
                             pady=20, 
                             padx=20, 
                             expand=True, 
                             fill = "both")
        
        self.name_label = ctk.CTkLabel(self.list_frame, 
                                       text="Guest Information",
                                       font=("Arial", 20, "bold"))
        self.name_label.grid(row=0, 
                             column=0, 
                             padx=20, 
                             pady=10, 
                             sticky="w")
        
        # Guest ID Label
        self.guest_id_label = ctk.CTkLabel(self.list_frame,
                                           text="Guest ID:",
                                           font=("Arial", 18, "bold"))
        self.guest_id_label.grid(row=1,
                                 column=0,
                                 padx=20,
                                 pady=(20,5),
                                 sticky="w")
        # Entry for Guest ID
        self.guest_id_entry = ctk.CTkEntry(self.list_frame,
                           width=200,
                           font=("Arial", 16))
        self.guest_id_entry.grid(row=2,
                     column=0,
                     padx=20,
                     pady=(5,20),
                     sticky="w",
                     columnspan=1)

        # Pre-fill Guest ID if guest_info is provided
        if guest_info is not None and len(guest_info) > 0:
            self.guest_id_entry.insert(0, guest_info[0]) # Assuming guest_info[0] is the Guest ID
            self.name_label.configure(text=f"Guest Name: {guest_info[0]}")  # Example of using guest name
        else:
            # Optionally, you can set default values or leave fields empty
            self.guest_id_entry.configure(state="normal")  # Ensure the entry is editable
            self.guest_id_entry.delete(0, "end")  # Clear any previous input if needed


        self.search_button = ctk.CTkButton(self.list_frame,
                           text="Search",
                           width=100,
                           font=("Arial", 16, "bold"))
        self.search_button.grid(row=2,
                       column=0,
                       padx=(230, 0),
                       pady=(5,20),
                       sticky="w")

        # Pax Label
        self.pax_label = ctk.CTkLabel(self.list_frame,
                  text="Pax:",
                  font=("Arial", 18, "bold"))
        self.pax_label.grid(row=1,
                column=1,
                padx=20,
                pady=(20,5),
                sticky="w")

        # Entry for Pax
        self.pax_entry = ctk.CTkEntry(self.list_frame,
                  width=100,
                  font=("Arial", 16))
        self.pax_entry.grid(row=2,
                column=1,
                padx=20,
                pady=(5,20),
                sticky="w",
                columnspan=1)
        
        # Special Request Label
        self.special_request_label = ctk.CTkLabel(self.list_frame,
            text="Special Request:",
            font=("Arial", 18, "bold"))
        self.special_request_label.grid(row=3,
            column=0,
            padx=20,
            pady=(10,5),
            sticky="w")

        # Entry for Special Request
        self.special_request_entry = ctk.CTkEntry(self.list_frame,
            width=650,
            height=50,
            font=("Arial", 16))
        self.special_request_entry.grid(row=4,
            column=0,
            padx=20,
            pady=(5,20),
            sticky="w",
            columnspan=5)
        
        # Reservation Details Frame
        self.reservation_details_frame = ctk.CTkFrame(self.list_frame, 
                                                      fg_color="transparent", 
                                                      width=900,
                                                      height=120)
        self.reservation_details_frame.configure(border_width=2,
                                                 border_color="#888888")
        self.reservation_details_frame.grid(
                            row=8, 
                            column=0, 
                            columnspan=5, 
                            padx=20, 
                            pady=(10, 20), 
                            sticky="ew")
        
        self.reservation_details_label = ctk.CTkLabel(
            self.list_frame,
            text="Reservation Details",
            font=("Arial", 20, "bold")
        )
        self.reservation_details_label.grid(
            row=7,
            column=0,
            columnspan=7,
            padx=20,
            pady=(0, 5),
            sticky="w"
        )

        # Check-in Date Label
        self.checkin_label = ctk.CTkLabel(self.reservation_details_frame, 
                                          text="Check-in Date:", 
                                          font=("Arial", 16, "bold"))
        self.checkin_label.grid(row=0, 
                                column=0, 
                                padx=10, 
                                pady=10, 
                                sticky="w")
        self.checkin_entry = ctk.CTkEntry(self.reservation_details_frame, 
                                          width=150, 
                                          font=("Arial", 15))
        self.checkin_entry.grid(row=0, 
                                column=1, 
                                padx=10, 
                                pady=10, 
                                sticky="w")

        # Check-out Date Label
        self.checkout_label = ctk.CTkLabel(self.reservation_details_frame,
                                           text="Check-out Date:",
                                           font=("Arial", 16, "bold"))
        self.checkout_label.grid(row=0,
                                 column=2,
                                 padx=10,
                                 pady=10,
                                 sticky="w")
        self.checkout_entry = ctk.CTkEntry(self.reservation_details_frame, 
                                           width=150, 
                                           font=("Arial", 15))
        self.checkout_entry.grid(row=0, 
                                 column=3, 
                                 padx=10, 
                                 pady=10, 
                                 sticky="w")

        # Room Type Label
        self.roomtype_label = ctk.CTkLabel(self.reservation_details_frame, 
                                           text="Room Type:", 
                                           font=("Arial", 16, "bold"))
        self.roomtype_label.grid(row=1, 
                                 column=0, 
                                 padx=10, 
                                 pady=10, 
                                 sticky="w")
        self.roomtype_combobox = ctk.CTkComboBox(self.reservation_details_frame, 
                                                 values=["Single", "Double", "Suite"],
                                                 width=150, 
                                                 font=("Arial", 15))
        self.roomtype_combobox.grid(row=1, 
                                    column=1, 
                                    padx=10, 
                                    pady=10, 
                                    sticky="w")

        # Room Number Label
        self.roomnumber_label = ctk.CTkLabel(self.reservation_details_frame, 
                                             text="Room Number:", 
                                             font=("Arial", 16, "bold"))
        self.roomnumber_label.grid(row=1, 
                                   column=2, 
                                   padx=10, 
                                   pady=10, 
                                   sticky="w")
        self.roomnumber_entry = ctk.CTkEntry(self.reservation_details_frame, 
                                             width=150, 
                                             font=("Arial", 15))
        self.roomnumber_entry.grid(row=1,
                                   column=3,
                                   padx=10,
                                   pady=10,
                                   sticky="w")
        
        # Amenities Label
        self.amenities_label = ctk.CTkLabel(
            self.reservation_details_frame,
            text="Amenities:",
            font=("Arial", 16, "bold")
        )
        self.amenities_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        # Amenities Display (readonly)
        self.amenities_text = ctk.CTkTextbox(
            self.reservation_details_frame,
            width=400,
            height=50,
            font=("Arial", 14),
            state="disabled",
            wrap="word"
        )
        self.amenities_text.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")

        # Example amenities for each room type
        self.room_amenities = {
            "Single": "1 Bed, Free WiFi, TV, Air Conditioning",
            "Double": "2 Beds, Free WiFi, TV, Air Conditioning, Mini Fridge",
            "Suite": "King Bed, Free WiFi, TV, Air Conditioning, Mini Fridge, Living Area, Jacuzzi"
        }

        def update_amenities(event=None):
            room_type = self.roomtype_combobox.get()
            amenities = self.room_amenities.get(room_type, "No amenities info available.")
            self.amenities_text.configure(state="normal")
            self.amenities_text.delete("1.0", "end")
            self.amenities_text.insert("1.0", amenities)
            self.amenities_text.configure(state="disabled")

        self.roomtype_combobox.bind("<<ComboboxSelected>>", update_amenities)
        update_amenities()
        
        # Add Another Room Button
        self.add_room_button = ctk.CTkButton(
            self.list_frame,
            text="Add Another Room",
            width=180,
            font=("Arial", 15, "bold"),
        )
        self.add_room_button.grid(
            row=9,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0, 10),
            sticky="w"
        ) #Put logic here that it adds another room to the reservation *Mapupunta sa other side*

        #Billing method
        self.name_label = ctk.CTkLabel(self.list_frame, 
                                       text="Billing Method",
                                       font=("Arial", 20, "bold"))
        self.name_label.grid(row=0, 
                             column=19, 
                             padx=20, 
                             pady=10, 
                            sticky="w")
    
        self.billing_method_text = ctk.CTkLabel(
            self.list_frame,
            text="Please select a billing method for this reservation.",
            font=("Arial", 15),
            text_color="#444444")
        
        self.billing_method_text.grid(
            row=1,
            column=19,
            padx=10,
            pady=(0, 10),
            sticky="we")
        
        self.billing_frame = ctk.CTkFrame(self.list_frame, 
                                                      fg_color="transparent", 
                                                      width=700,
                                                      height=70)
        self.billing_frame.configure(border_width=2,
                                                 border_color="#888888")
        self.billing_frame.grid(
                            row=2, 
                            column=19, 
                            columnspan=2, 
                            padx=20, 
                            pady=(10, 20), 
                            sticky="w")
        # Payment Method Label
        self.payment_method_label = ctk.CTkLabel(
            self.billing_frame,
            text="Payment Method:",
            font=("Arial", 16, "bold")
        )
        self.payment_method_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Payment Method Combobox
        self.payment_method_combobox = ctk.CTkComboBox(
            self.billing_frame,
            values=["Cash", "Credit Card", "Debit Card", "Bank Transfer"],
            width=180,
            font=("Arial", 15)
        )
        self.payment_method_combobox.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Downpayment Label
        self.downpayment_label = ctk.CTkLabel(
            self.billing_frame,
            text="Downpayment:",
            font=("Arial", 16, "bold")
        )
        self.downpayment_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Downpayment Entry
        self.downpayment_combobox = ctk.CTkComboBox(
            self.billing_frame,
            values=["50% Downpayment", "100% Full Payment"], #Placeholder values
            width=180,
            font=("Arial", 15)
        )
        self.downpayment_combobox.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        
        #----------------------------------
        # Buttons inside the CreateReservation frame
        self.bottom_frame = ctk.CTkFrame(self, 
                         fg_color="transparent", 
                         height=100)
        self.bottom_frame.pack(side="bottom", 
                       pady=(10, 20), 
                       padx=20, 
                       fill="x")

        # Create Reservation Button
        self.create_button = ctk.CTkButton(
            self.bottom_frame,
            text="Create Reservation",
            width=200,
            height=40,
            font=("Arial", 16, "bold"))
        self.create_button.pack(side="right", padx=20)

        def show_invoice_loading():
            loading_popup = ctk.CTkToplevel(self)
            loading_popup.title("Loading Invoice")
            loading_popup.geometry("350x120")
            loading_popup.grab_set()
            label = ctk.CTkLabel(loading_popup, text="Invoice loading...", font=("Arial", 18, "bold"))
            label.pack(expand=True, pady=30)
            # Optionally, you can add a progress bar or spinner here

        self.create_button.configure(command=show_invoice_loading)

        # Cancel Button
        self.cancel_button = ctk.CTkButton(
            self.bottom_frame,
            text="Cancel",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.master.destroy,
            fg_color="#b0b0b0"
        )
        self.cancel_button.pack(side="right", padx=10)


#temp display
if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("light")
    app = CreateReservation(root)
    app.pack(fill="both",
             expand=True)
    root.mainloop()