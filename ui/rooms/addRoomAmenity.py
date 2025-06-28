import customtkinter as ctk
from tkinter import messagebox

from models.room import RoomModel
from ui.components.customDropdown import CustomDropdown
from utils.helpers import log


class AddRoomAmenityFrame(ctk.CTkFrame):
    BG_COLOR_1 = "#F7F7F7"
    BG_COLOR_2 = "white"
    FONT_HEADER = ("Roboto Condensed", 24)
    FONT_LABEL = ("Roboto", 14)
    FONT_ENTRY = ("Roboto", 10)
    FONT_ENTRY_LABEL = ("Roboto", 12)
    TEXT_COLOR_LABEL = "black"
    TEXT_COLOR_ENTRY = "#818197"
    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 30
    BORDER_WIDTH = 1
    BORDER_COLOR = "#b5b5b5"
    SEPERATOR_COLOR = "#D3D3D3"
    PADX_LABEL = (20, 20)

    def __init__(self, parent_popup, parent_page=None):
        super().__init__(parent_popup)
        self.configure(fg_color=self.BG_COLOR_2)
        self.parent_page = parent_page
        self.room_model = RoomModel()

        self.entries = {}

        self.create_widgets()


    def create_widgets(self):
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR_2, corner_radius=0)
        header_frame.pack(fill="x")

        header = ctk.CTkLabel(header_frame, text="Add Room Amenity", font=self.FONT_HEADER, text_color="black")
        header.pack(pady=(20, 20))

        bottom_border = ctk.CTkFrame(header_frame, height=1, fg_color=self.SEPERATOR_COLOR, border_width=1)
        bottom_border.pack(fill="x", side="bottom")

        # ========== Form Frame with 2 Columns ==========
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=20, pady=(50, 20), fill="both", expand=True)

        # ========== Amenity Name ==========
        label = ctk.CTkLabel(form_frame, text="Amenity Name *", font=self.FONT_LABEL,
                             text_color=self.TEXT_COLOR_LABEL)
        label.grid(row=0, column=0, sticky="nw", padx=self.PADX_LABEL, pady=10)
        frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        frame.grid(row=0, column=1, sticky="w", padx=(20, 20), pady=(10, 0))
        entry = ctk.CTkEntry(frame, width=self.ENTRY_WIDTH, height=self.ENTRY_HEIGHT, fg_color=self.BG_COLOR_2,
                             border_width=self.BORDER_WIDTH, border_color=self.BORDER_COLOR)
        entry.grid(row=0, column=0, sticky="w")
        label_entry = ctk.CTkLabel(frame, text="Eg : Television , Wifi", font=self.FONT_ENTRY_LABEL,
                                   text_color=self.TEXT_COLOR_ENTRY)
        label_entry.grid(row=1, column=0, sticky="nw")
        self.entries["entry_amenity_name"] = entry


        # ========== Button Frame ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=6, column=1, padx=(20, 0), pady=(50, 20), sticky="ew")

        # ========== Submit Button ==========
        self.submit_button = ctk.CTkButton(button_frame, text="Add", command=self.on_submit,
                                           height=30, width=80)
        self.submit_button.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # ========== Rest Button ==========
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", command=self.reset_form,
                                          height=30, width=80, fg_color=self.BG_COLOR_2, text_color="black",
                                          border_width=1, border_color=self.BORDER_COLOR)
        self.reset_button.grid(row=0, column=2, sticky="w")


    def on_submit(self):
        amenity_name = self.entries["entry_amenity_name"].get().strip()

        if not amenity_name:
            messagebox.showerror("Error", "Amenity Name cannot be empty.")
            return

        try:
            amenity_id = self.room_model.add_amenity(amenity_name)
            if amenity_id:
                messagebox.showinfo("Success", f"Amenity '{amenity_name}' added successfully with ID {amenity_id}.")

                if self.parent_page:
                    self.parent_page.refresh_amenities()

                # Focus on parent after message is dismissed
                if self.parent_page and hasattr(self.parent_page.master, "lift"):
                    self.parent_page.master.attributes("-topmost", True)
                    self.parent_page.master.focus_force()
                    self.parent_page.master.after(100, lambda: self.parent_page.master.attributes("-topmost", False))

                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to add amenity. It may already exist.")
        except Exception as e:
            log(f"Error adding amenity: {e}")
            messagebox.showerror("Error", f"An error occurred while adding the amenity: {e}")


    def reset_form(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        log("Form reset successfully.")
        messagebox.showinfo("Reset", "Form has been reset successfully.")
