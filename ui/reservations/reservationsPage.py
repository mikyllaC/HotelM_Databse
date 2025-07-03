import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

from models.guest import GuestModel
from models.reservation import ReservationModel
from utils.helpers import log

class ReservationsPage(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    TITLE_COLOR = "#303644"
    TREE_HEADER_FONT = ("Roboto Condensed", 11, "bold")
    TREE_FONT = ("Roboto Condensed", 11)
    TREE_SELECT_COLOR = "#DEECF7"

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=self.BG_COLOR_1)
        self.guest_model = GuestModel()
        self.reservation_model = ReservationModel()

        # Updated column headers for the reservation table
        self.reservation_data = [
            ["Reservation ID", "Check In", "Check Out", "Guest Name", "Room Number", "Status"]
        ]

        self.create_widgets()
        self.populate_reservations()


    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Reservation Management", font=("Roboto Condensed", 28, "bold"),
                                   text_color=self.TITLE_COLOR)
        title_label.pack(anchor="nw", pady=(20, 20), padx=(35, 0))

        # Action Bar Frame
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(anchor="n", padx=(35, 0), fill="x")

        # Create Reservation Button
        create_reservation_button = ctk.CTkButton(
            self.action_frame,
            text="Create Reservation",
            font=("Roboto Condensed", 16, "bold"),
            width=180,
            height=36,
            command=self.create_reservation_popup
        )
        create_reservation_button.pack(side="left", padx=(0, 10))

        # Search Entry with auto-filter
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.filter_table())
        self.search_entry = ctk.CTkEntry(
            self.action_frame,
            width=220,
            height=36,
            placeholder_text="Search guest name...",
            textvariable=self.search_var,
            font=("Roboto Condensed", 14)
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        # Filter Combobox
        self.filter_var = StringVar(value="All Status")
        self.filter_combobox = ctk.CTkComboBox(
            self.action_frame,
            width=160,
            height=36,
            values=["All Status", "Booked", "Confirmed", "Checked In", "Checked Out", "Cancelled"],
            variable=self.filter_var,
            font=("Roboto Condensed", 14),
            command=lambda x: self.filter_table()
        )
        self.filter_combobox.pack(side="left", padx=(0, 10))

        # Table Frame
        self.table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.table_frame.pack_propagate(False)
        self.table_frame.pack(padx=(10, 10), pady=(15, 10), fill="both", expand=True, anchor="n")

        # Right Frame for reservation details
        self.right_frame = ctk.CTkFrame(self, width=300, fg_color=self.BG_COLOR_2,
                                        border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        # Initially hidden
        self.right_frame.place_forget()

        # Treeview for displaying reservations
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.TREE_HEADER_FONT, anchor="w")
        style.configure("Treeview", rowheight=35, font=self.TREE_FONT, anchor="w")
        style.map("Treeview",
                  background=[('selected', self.TREE_SELECT_COLOR)],
                  foreground=[('selected', "black")])

        self.treeview = ttk.Treeview(self.table_frame, columns=self.reservation_data[0], show="headings")
        self.treeview.pack(expand=True, fill="both")
        self.treeview.tag_configure('oddrow', background='#f5f5f5')
        self.treeview.tag_configure('evenrow', background='white')

        # Set column headings and widths
        for col in self.reservation_data[0]:
            self.treeview.heading(col, text=col, anchor="w")
            self.treeview.column(col, anchor="w", width=100, stretch=True)

        # Customize column widths
        self.treeview.column("Reservation ID", width=100, anchor="w")
        self.treeview.column("Check In", width=50, anchor="w")
        self.treeview.column("Check Out", width=50, anchor="w")
        self.treeview.column("Guest Name", width=200, anchor="w")
        self.treeview.column("Room Number", width=100, anchor="w")
        self.treeview.column("Status", width=150, anchor="w")

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Bind row selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)


    def populate_reservations(self):
        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        try:
            # Get reservations from the database using the reservation model
            reservations = self.reservation_model.get_all_reservations()

            if not reservations:
                log("No reservations found in database")
                self.treeview.insert("", "end", values=("-", "-", "-", "-", "-", "-"))
                return

            # For each reservation, get the guest and room details
            for i, reservation in enumerate(reservations):
                guest_id = reservation.get("GUEST_ID")
                room_id = reservation.get("ROOM_ID")
                guest_name = "Unknown Guest"
                room_number = "N/A"

                # Try to get guest details if available
                try:
                    guest = self.guest_model.get_guest_by_id(guest_id)
                    if guest:
                        guest_name = f"{guest.get('FIRST_NAME', 'Guest')} {guest.get('LAST_NAME', '')}"
                except Exception as e:
                    log(f"Could not get guest details for ID {guest_id}: {str(e)}", "WARNING")

                # Try to get room details
                try:
                    from models.room import RoomModel
                    room_model = RoomModel()
                    room_data = room_model.get_room_data_with_type(room_id)
                    if room_data:
                        room_number = room_data.get('ROOM_NUMBER', 'N/A')
                except Exception as e:
                    log(f"Could not get room details for ID {room_id}: {str(e)}", "WARNING")

                # Format dates for display
                check_in_date = reservation.get("CHECK_IN_DATE", "N/A")
                check_out_date = reservation.get("CHECK_OUT_DATE", "N/A")

                # Prepare values for table with new column structure
                values = (
                    f"R{reservation.get('RESERVATION_ID', 0)}",  # Reservation ID
                    check_in_date,  # Check In
                    check_out_date,  # Check Out
                    guest_name,  # Guest Name
                    room_number,  # Room Number
                    reservation.get("STATUS", "Booked")  # Status
                )

                # Add to treeview with alternating row colors
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                item_id = self.treeview.insert("", "end", values=values, tags=(tag,))

                # Store the reservation ID as an item attribute for later retrieval
                self.treeview.item(item_id, tags=(tag, f"res_{reservation.get('RESERVATION_ID', 0)}"))

        except Exception as e:
            log(f"Error populating reservations: {str(e)}", "ERROR")
            self.treeview.insert("", "end", values=("Error loading reservations", "", "", "", "", ""))


    def filter_table(self):
        search_text = self.search_var.get().lower().strip()
        selected_status = self.filter_var.get()

        # Clear existing items
        self.treeview.delete(*self.treeview.get_children())

        try:
            # Get all reservations first
            reservations = self.reservation_model.get_all_reservations()
            if not reservations:
                log("No reservations found in database")
                self.treeview.insert("", "end", values=("-", "-", "-", "-", "-", "-"))
                return

            # Filter by status if needed
            if selected_status != "All Status":
                reservations = [r for r in reservations if r.get("STATUS") == selected_status]

            # Process each reservation
            filtered_count = 0
            for i, reservation in enumerate(reservations):
                guest_id = reservation.get("GUEST_ID")
                room_id = reservation.get("ROOM_ID")
                guest_name = "Unknown Guest"
                room_number = "N/A"

                # Try to get guest details if available
                try:
                    guest = self.guest_model.get_guest_by_id(guest_id)
                    if guest:
                        guest_name = f"{guest.get('FIRST_NAME', 'Guest')} {guest.get('LAST_NAME', '')}"
                except Exception as e:
                    log(f"Could not get guest details for ID {guest_id}: {str(e)}", "WARNING")

                # Apply search filter on guest name
                if search_text and search_text not in guest_name.lower():
                    continue

                # Try to get room details
                try:
                    from models.room import RoomModel
                    room_model = RoomModel()
                    room_data = room_model.get_room_data_with_type(room_id)
                    if room_data:
                        room_number = room_data.get('ROOM_NUMBER', 'N/A')
                except Exception as e:
                    log(f"Could not get room details for ID {room_id}: {str(e)}", "WARNING")

                # Format dates for display
                check_in_date = reservation.get("CHECK_IN_DATE", "N/A")
                check_out_date = reservation.get("CHECK_OUT_DATE", "N/A")

                # Prepare values for table with new column structure
                values = (
                    f"R{reservation.get('RESERVATION_ID', 0)}",  # Reservation ID
                    check_in_date,  # Check In
                    check_out_date,  # Check Out
                    guest_name,  # Guest Name
                    room_number,  # Room Number
                    reservation.get("STATUS", "Booked")  # Status
                )

                # Add to treeview with alternating row colors
                tag = 'evenrow' if filtered_count % 2 == 0 else 'oddrow'
                item_id = self.treeview.insert("", "end", values=values, tags=(tag,))

                # Store the reservation ID as an item attribute for later retrieval
                self.treeview.item(item_id, tags=(tag, f"res_{reservation.get('RESERVATION_ID', 0)}"))
                filtered_count += 1

            # If no results after filtering
            if filtered_count == 0:
                self.treeview.insert("", "end", values=("No matching reservations", "", "", "", "", ""))

        except Exception as e:
            log(f"Error filtering reservations: {str(e)}", "ERROR")
            self.treeview.insert("", "end", values=("Error filtering reservations", "", "", "", "", ""))


    def show_reservation_info(self, reservation_values):
        # Clear existing widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Set up header with navigation and controls
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                    border_width=0, border_color=self.BORDER_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(3, 0))
        header_frame.grid_columnconfigure(0, weight=1)

        # Right Header Frame with buttons
        right_header_frame = ctk.CTkFrame(header_frame, fg_color=self.BG_COLOR_2)
        right_header_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="e")

        # Get reservation ID from the selected item's tags
        selected_item = self.treeview.selection()[0]
        item_tags = self.treeview.item(selected_item, "tags")
        reservation_id = None

        # Extract reservation ID from tags
        for tag in item_tags:
            if tag.startswith("res_"):
                try:
                    reservation_id = int(tag[4:])
                except ValueError:
                    pass
                break

        # Edit and Cancel buttons
        edit_button = ctk.CTkButton(right_header_frame, text="Edit", text_color="black", width=50, height=30,
                                   corner_radius=4, fg_color=self.BG_COLOR_2,
                                   border_width=1, border_color=self.BORDER_COLOR,
                                   command=lambda: self.edit_reservation_popup(reservation_id))
        edit_button.grid(column=0, row=0, padx=(0, 5))

        cancel_button = ctk.CTkButton(right_header_frame, text="Cancel", text_color="black", width=50, height=30,
                                     corner_radius=4, fg_color="#ffcccc",
                                     border_width=1, border_color=self.BORDER_COLOR,
                                     command=lambda: self.cancel_reservation_popup(reservation_id))
        cancel_button.grid(column=1, row=0, padx=(0, 5))

        # Delete button - initially disabled, will be enabled only for cancelled reservations
        self.delete_button = ctk.CTkButton(right_header_frame, text="Delete", text_color="white", width=50, height=30,
                                     corner_radius=4, fg_color="#dc3545", hover_color="#c82333",
                                     border_width=1, border_color=self.BORDER_COLOR,
                                     command=lambda: self.delete_reservation(reservation_id))
        self.delete_button.grid(column=2, row=0, padx=(0, 5))

        exit_button = ctk.CTkButton(right_header_frame, text="X", text_color="black", width=10, height=10,
                                   corner_radius=4, fg_color=self.BG_COLOR_2, border_width=0,
                                   command=lambda: [self.right_frame.place_forget(),
                                                   self.treeview.selection_remove(self.treeview.selection())],
                                   font=("Grizzly BT", 16), hover_color=self.BG_COLOR_2)
        exit_button.grid(column=3, row=0, padx=(5, 10))

        # Bottom Header Border
        bottom_border = ctk.CTkFrame(header_frame, height=0, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Content in a scrollable frame
        scrollable = ctk.CTkScrollableFrame(self.right_frame, fg_color=self.BG_COLOR_2, corner_radius=0)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))
        scrollable.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        title_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Reservation Details", font=("Roboto Condensed", 18))
        title_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        bottom_border = ctk.CTkFrame(title_frame, height=1, fg_color="#D3D3D3", border_width=1)
        bottom_border.grid(row=1, column=0, sticky="ew", padx=(0, 0), pady=(10, 0))

        # Reservation Information
        info_frame = ctk.CTkFrame(scrollable, fg_color=self.BG_COLOR_2)
        info_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Get reservation details from database
        extended_info = {}
        try:
            if reservation_id:
                # Get reservation details from the database
                reservation = self.reservation_model.get_reservation_by_id(reservation_id)
                if reservation:
                    # Get guest details
                    guest_details = {"FIRST_NAME": "Guest", "LAST_NAME": str(reservation.get("GUEST_ID")), "CONTACT_NUMBER": "N/A", "EMAIL": "N/A"}
                    try:
                        guest = self.guest_model.get_guest_by_id(reservation.get("GUEST_ID"))
                        if guest:
                            guest_details = guest
                    except Exception as e:
                        log(f"Could not get guest details: {str(e)}", "WARNING")

                    # Get room details
                    room_id = reservation.get("ROOM_ID")
                    room_number = "N/A"
                    room_type = "N/A"

                    try:
                        from models.room import RoomModel
                        room_model = RoomModel()
                        room_data = room_model.get_room_data_with_type(room_id)
                        if room_data:
                            room_number = room_data.get('ROOM_NUMBER', 'N/A')
                            room_type = room_data.get('TYPE_NAME', 'N/A')
                    except Exception as e:
                        log(f"Could not get room details for ID {room_id}: {str(e)}", "WARNING")

                    # Calculate number of nights
                    from datetime import datetime
                    try:
                        check_in = datetime.strptime(reservation.get("CHECK_IN_DATE"), "%Y-%m-%d")
                        check_out = datetime.strptime(reservation.get("CHECK_OUT_DATE"), "%Y-%m-%d")
                        num_nights = (check_out - check_in).days
                    except:
                        num_nights = "N/A"

                    # Build extended info dictionary
                    extended_info = {
                        "Reservation ID": f"R{reservation.get('RESERVATION_ID')}",
                        "Guest Name": f"{guest_details.get('FIRST_NAME', 'Guest')} {guest_details.get('LAST_NAME', '')}",
                        "Guest ID": reservation.get("GUEST_ID"),
                        "Phone": guest_details.get("CONTACT_NUMBER", "N/A"),
                        "Email": guest_details.get("EMAIL", "N/A"),
                        "Room Number": room_number,
                        "Room Type": room_type,
                        "Check-in Date": reservation.get("CHECK_IN_DATE"),
                        "Check-out Date": reservation.get("CHECK_OUT_DATE"),
                        "Number of Nights": num_nights,
                        "Number of Adults": reservation.get("NUMBER_OF_ADULTS", "1"),
                        "Number of Children": reservation.get("NUMBER_OF_CHILDREN", "0"),
                        "Special Requests": reservation.get("NOTES", "None"),
                        "Status": reservation.get("STATUS", "Booked"),
                    }

                    # Store the reservation status in a class variable for the delete button to access
                    self.current_reservation_status = reservation.get("STATUS", "Booked")
        except Exception as e:
            log(f"Error getting reservation details: {str(e)}", "ERROR")
            extended_info = {
                "Reservation ID": "Error",
                "Error Message": f"Could not load reservation details: {str(e)}"
            }

        # If we couldn't get reservation details from the database, use the values from the treeview
        if not extended_info:
            extended_info = {
                "Reservation ID": "Unknown",
                "Guest Name": reservation_values[0],
                "Guest ID": reservation_values[1],
                "Phone": reservation_values[2],
                "Email": f"{reservation_values[0].split()[0].lower()}@example.com",
                "Number of Rooms": reservation_values[3],
                "Status": reservation_values[4],
                "Note": "Complete reservation details could not be loaded"
            }

        # Add info rows
        info_rows = [(key, value) for key, value in extended_info.items()]

        info_frame.grid_columnconfigure(0, minsize=150, weight=1, uniform="info")
        info_frame.grid_columnconfigure(1, minsize=200, weight=1, uniform="info")

        # Create labels for each information row
        for index, (label, value) in enumerate(info_rows):
            # Label "cell" frame
            label_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_1, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            label_cell.grid(row=index, column=0, sticky="nsew")

            # Value "cell" frame
            value_cell = ctk.CTkFrame(info_frame, fg_color=self.BG_COLOR_2, corner_radius=0,
                                      border_width=1, border_color=self.BORDER_COLOR)
            value_cell.grid(row=index, column=1, sticky="nsew")

            # Label text
            label_text = ctk.CTkLabel(label_cell, text=label, font=("Roboto", 13), anchor="w",
                                      wraplength=140, justify="left")
            label_text.pack(fill="both", expand=True, padx=10, pady=10)

            # Value text
            value_text = ctk.CTkLabel(value_cell, text=str(value), font=("Roboto", 13),
                                      anchor="w", wraplength=190, justify="left")
            value_text.pack(fill="both", expand=True, padx=10, pady=10)


    def on_row_select(self, event):
        selected_item = self.treeview.selection()

        if selected_item:
            reservation_values = self.treeview.item(selected_item[0], "values")
            if reservation_values and reservation_values[0] != "-":
                self.right_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.50, relheight=1)
                self.show_reservation_info(reservation_values)
        else:
            self.right_frame.place_forget()


    def create_reservation_popup(self):
        from ui.reservations.createReservation import CreateReservation

        popup = ctk.CTkToplevel(self)
        popup.title("Create Reservation")
        popup.geometry("1300x500")
        popup.grab_set()

        frame = CreateReservation(popup, parent_page=self)
        frame.pack(fill="both", expand=True)


    def refresh_data(self):
        """Refresh the reservations table after creating/updating a reservation"""
        self.populate_reservations()

    def edit_reservation_popup(self, reservation_id=None):
        # Get reservation ID if not provided
        if not reservation_id:
            selected_item = self.treeview.selection()
            if not selected_item:
                return

            # Get reservation ID from item tags
            item_tags = self.treeview.item(selected_item[0], "tags")
            for tag in item_tags:
                if tag.startswith("res_"):
                    try:
                        reservation_id = int(tag[4:])
                    except ValueError:
                        pass
                    break

        if not reservation_id:
            messagebox.showerror("Error", "Could not determine which reservation to edit.")
            return

        try:
            from ui.reservations.editReservation import EditReservation

            popup = ctk.CTkToplevel(self)
            popup.title(f"Edit Reservation #{reservation_id}")
            popup.geometry("1300x500")
            popup.grab_set()

            frame = EditReservation(popup, reservation_id, parent_page=self)
            frame.pack(fill="both", expand=True)

        except Exception as e:
            log(f"Error opening edit reservation popup: {str(e)}")
            messagebox.showerror("Error", f"Could not open edit window: {str(e)}")

    def cancel_reservation_popup(self, reservation_id=None):
        # Get reservation ID if not provided
        if not reservation_id:
            selected_item = self.treeview.selection()
            if not selected_item:
                return

            # Get reservation ID from item tags
            item_tags = self.treeview.item(selected_item[0], "tags")
            for tag in item_tags:
                if tag.startswith("res_"):
                    try:
                        reservation_id = int(tag[4:])
                    except ValueError:
                        pass
                    break

        if not reservation_id:
            messagebox.showerror("Error", "Could not determine which reservation to cancel.")
            return

        # Try to get reservation details for confirmation
        try:
            reservation = self.reservation_model.get_reservation_by_id(reservation_id)
            if not reservation:
                messagebox.showerror("Error", f"Reservation with ID {reservation_id} not found.")
                return

            # Get guest name for confirmation message
            guest_name = "Unknown Guest"
            try:
                guest = self.guest_model.get_guest_by_id(reservation.get("GUEST_ID"))
                if guest:
                    guest_name = f"{guest.get('FIRST_NAME', '')} {guest.get('LAST_NAME', '')}"
            except:
                pass

            # Check if the reservation has been paid and might need a refund
            from models.billing import BillingModel
            billing_model = BillingModel()
            payment_status = billing_model.check_payment_status_for_reservation(reservation_id)

            # If the reservation has been paid, warn about refund requirement
            if payment_status['has_payments']:
                messagebox.showinfo(
                    "Payment Found",
                    f"This reservation has payments of ${payment_status['amount']:.2f}.\n\n" +
                    "You must process a refund in the Billing section before cancelling this reservation."
                )
                return

            # Create confirmation dialog
            cancel_window = ctk.CTkToplevel(self)
            cancel_window.title("Cancel Reservation")
            cancel_window.geometry("400x350")
            cancel_window.grab_set()
            cancel_window.configure(fg_color=self.BG_COLOR_2)

            ctk.CTkLabel(cancel_window, text="Cancel Reservation",
                         font=("Roboto Condensed", 20, "bold")).pack(pady=(20, 10))

            ctk.CTkLabel(cancel_window,
                         text=f"Are you sure you want to cancel the reservation for {guest_name}?",
                         font=("Roboto Condensed", 14),
                         wraplength=350,
                         justify="center").pack(pady=(10, 10))

            # Show reservation details
            details_text = f"Reservation ID: R{reservation_id}\n" \
                           f"Check-in: {reservation.get('CHECK_IN_DATE')}\n" \
                           f"Check-out: {reservation.get('CHECK_OUT_DATE')}\n" \
                           f"Status: {reservation.get('STATUS')}"

            ctk.CTkLabel(cancel_window, text=details_text,
                         font=("Roboto Condensed", 13),
                         wraplength=350,
                         justify="center").pack(pady=(0, 20))

            # Reason entry
            ctk.CTkLabel(cancel_window, text="Cancellation Reason:",
                         font=("Roboto Condensed", 14),
                         anchor="w").pack(pady=(0, 5), padx=(40, 40), anchor="w")

            reason_entry = ctk.CTkEntry(cancel_window, width=320, height=30)
            reason_entry.pack(pady=(0, 20), padx=(40, 40))

            # Button frame
            button_frame = ctk.CTkFrame(cancel_window, fg_color="transparent")
            button_frame.pack(pady=(0, 20))

            def confirm_cancel():
                # Cancel the reservation in the database
                reason = reason_entry.get()
                success = self.reservation_model.cancel_reservation(reservation_id, reason)

                if success:
                    # Refresh the table to reflect the changes
                    self.refresh_data()

                    # Close the right panel if it's showing this reservation
                    self.right_frame.place_forget()

                    # Show confirmation
                    messagebox.showinfo("Success", f"Reservation for {guest_name} has been cancelled.")
                else:
                    messagebox.showerror("Error", "Failed to cancel the reservation. Please try again.")

                cancel_window.destroy()

            # Add buttons
            ctk.CTkButton(button_frame, text="Cancel Reservation",
                          fg_color="#e74c3c", hover_color="#c0392b",
                          command=confirm_cancel).pack(side="left", padx=10)

            ctk.CTkButton(button_frame, text="Back",
                          fg_color="#3498db", hover_color="#2980b9",
                          command=cancel_window.destroy).pack(side="left", padx=10)

        except Exception as e:
            log(f"Error preparing cancellation dialog: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not load reservation details: {str(e)}")

    def delete_reservation(self, reservation_id=None):
        # Get reservation ID if not provided
        if not reservation_id:
            selected_item = self.treeview.selection()
            if not selected_item:
                return

            # Get reservation ID from item tags
            item_tags = self.treeview.item(selected_item[0], "tags")
            for tag in item_tags:
                if tag.startswith("res_"):
                    try:
                        reservation_id = int(tag[4:])
                    except ValueError:
                        pass
                    break

        if not reservation_id:
            messagebox.showerror("Error", "Could not determine which reservation to delete.")
            return

        # Get the current reservation details
        try:
            reservation = self.reservation_model.get_reservation_by_id(reservation_id)
            if not reservation:
                messagebox.showerror("Error", f"Reservation with ID {reservation_id} not found.")
                return

            # Check if the reservation is cancelled
            if reservation.get("STATUS") != "Cancelled":
                messagebox.showwarning(
                    "Cannot Delete Reservation",
                    "Only cancelled reservations can be deleted.\n\n" +
                    f"The current status is: {reservation.get('STATUS')}\n\n" +
                    "Cancel the reservation first before attempting to delete it."
                )
                return

            # If we get here, the reservation is cancelled, so we can proceed with deletion
            # Confirmation dialog
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this cancelled reservation? This action cannot be undone.",
                icon="warning"
            )

            if confirm:
                # Delete the reservation from the database
                success = self.reservation_model.delete_reservation(reservation_id)

                if success:
                    # Refresh the reservations list
                    self.refresh_data()

                    # Close the right panel if it's showing this reservation
                    self.right_frame.place_forget()

                    messagebox.showinfo("Deleted", "Reservation deleted successfully.")
                else:
                    messagebox.showerror("Error", "Failed to delete the reservation. Please try again.")

        except Exception as e:
            log(f"Error deleting reservation: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Could not delete reservation: {str(e)}")
