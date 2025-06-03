import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class AddStaffFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Add Staff")
        self.master.geometry("1600x800")
        self.master.configure(bg="#ffffff")
        ctk.set_appearance_mode("light")

        label = ctk.CTkLabel(self, 
                             text="Add Staff", 
                             font=("Arial", 24, "bold")
    )
        label.pack(pady=(30,60))

        form_frame = ctk.CTkFrame(self, 
                                  fg_color="#AAA7A7", 
                                  corner_radius=10, 
                                  height=1080, 
                                  width=1200) 
        form_frame.pack(pady=(10,10), 
                        padx=(40,40), 
                        fill="x", 
                        expand=False)
        form_frame.pack_propagate(False)  # Prevent frame from shrinking to fit its contents *Still shrinks, still fixing it

        #First Name Name
        Fname_label = ctk.CTkLabel(form_frame, text="First Name", 
                                  font=("Arial", 18, "bold"))
        Fname_label.grid(row=0, column=0, 
                        padx=(20, 10), 
                        pady=(20, 0), 
                        sticky="w", 
                        columnspan=2)
        Fname_entry = ctk.CTkEntry(form_frame, 
                                  width=200, 
                                  font=("Arial", 16))
        Fname_entry.grid(row=1, 
                        column=0, 
                        padx=(20, 10), 
                        pady=(0, 20), 
                        sticky="w", 
                        columnspan=2)

        #Last Name
        Lname_label = ctk.CTkLabel(form_frame, 
                       text="Last Name", 
                       font=("Arial", 18, "bold"))
        Lname_label.grid(row=0, 
             column=2, 
             padx=(20, 10), 
             pady=(20, 0), 
             sticky="w", 
             columnspan=2)
        Lname_entry = ctk.CTkEntry(form_frame, 
                       width=200, 
                       font=("Arial", 16))
        Lname_entry.grid(row=1, 
                 column=1, 
                 padx=(20, 10), 
                 pady=(0, 20), 
                 sticky="w", 
                 columnspan=2)
        
        Lname_entry.grid(row=1, 
                      column=2, 
                      padx=(20, 10), 
                      pady=(0, 20), 
                      sticky="w", 
                      columnspan=2)
        
        
        #Date of Birth
        dob_label = ctk.CTkLabel(form_frame, text="Date of Birth", 
                     font=("Arial", 18, "bold"))
        dob_label.grid(row=0, 
                    column=5, 
                   padx=(20, 10), 
                   pady=(20, 0), 
                   sticky="w", 
                   columnspan=2)
        dob_entry = ctk.CTkEntry(form_frame, 
                     width=200, 
                     font=("Arial", 16), 
                     placeholder_text="YYYY-MM-DD")
        dob_entry.grid(row=1, 
                   column=5, 
                   padx=(20, 10), 
                   pady=(0, 20), 
                   sticky="w", 
                   columnspan=2)
        

        #Contact Number
        contact_label = ctk.CTkLabel(form_frame, text="Contact Number", 
                                  font=("Arial", 18, "bold"))
        contact_label.grid(row=3, 
                           column=0, 
                        padx=(20, 10), 
                        pady=(20, 0), 
                        sticky="w", 
                        columnspan=2)
        contact_entry = ctk.CTkEntry(form_frame, 
                                  width=200, 
                                  font=("Arial", 16))
        contact_entry.grid(row=4, 
                        column=0, 
                        padx=(20, 10), 
                        pady=(0, 20), 
                        sticky="w", 
                        columnspan=2)

        # Email
        email_label = ctk.CTkLabel(form_frame, text="Email", 
                      font=("Arial", 18, "bold"))
        email_label.grid(row=3, 
                 column=2, 
                 padx=(20, 10), 
                 pady=(20, 0), 
                 sticky="w", 
                 columnspan=2)
        email_entry = ctk.CTkEntry(form_frame, 
                      width=200, 
                      font=("Arial", 16))
        email_entry.grid(row=4, 
                 column=2, 
                 padx=(20, 10), 
                 pady=(0, 20), 
                 sticky="w", 
                 columnspan=2)
        
        # Address Entry
        address_label = ctk.CTkLabel(form_frame, 
                         text="Address", 
                         font=("Arial", 18, "bold"))
        address_label.grid(row=5, 
                   column=0, 
                   padx=(20, 10),
                   pady=(20, 0), 
                   sticky="w", 
                   columnspan=2)
        address_entry = ctk.CTkEntry(form_frame, 
             width=250,
             font=("Arial", 16))
        address_entry.grid_configure(columnspan=10)  # Span more columns to make it visually longer
        address_entry.grid(row=6, 
                   column=0, 
                   padx=(20, 10), 
                   pady=(0, 20), 
                   sticky="w", 
                   columnspan=2)



        # Position 
        position_label = ctk.CTkLabel(form_frame, 
                          text="Position:", 
                          font=("Arial", 18, "bold"))
        position_label.grid(row=7, 
                    column=0, 
                    padx=(20, 10), 
                    pady=(20, 0), 
                    sticky="w", 
                    columnspan=2)
        position_options = ["Manager",      #Temp list of positions
                    "Receptionist", 
                    "Housekeeping", 
                    "Chef", 
                    "Waiter", 
                    "Security"]
        position_var = tk.StringVar(value=position_options[0])
        position_dropdown = ctk.CTkComboBox(form_frame, 
                            values=position_options, 
                            variable=position_var, 
                            width=250, 
                            font=("Courier", 16))
        position_dropdown.grid(row=8, 
                       column=0, 
                       padx=(20, 10), 
                       pady=(0, 20), 
                       sticky="w", 
                       columnspan=2)
        
        # Employee ID
        emp_id_label = ctk.CTkLabel(form_frame,
            text="Employee ID",
            font=("Arial", 18, "bold"))
        emp_id_label.grid(row=7,
            column=2,
            padx=(20, 10),
            pady=(20, 0),
            sticky="w",
            columnspan=2)
        emp_id_entry = ctk.CTkEntry(form_frame,
            width=200,
            font=("Arial", 16))
        emp_id_entry.grid(row=8,
            column=2,
            padx=(20, 10),
            pady=(0, 20),
            sticky="w",
            columnspan=2)
   
    #Frame for button
        below_frame = ctk.CTkFrame(self, 
                                   fg_color="transparent", 
                                   corner_radius=10)
        below_frame.pack(pady=(20, 10), 
                         padx=(40, 40), 
                         fill="x", 
                         expand=False)
        below_frame.configure(height=150)

        #Add button
        add_button = ctk.CTkButton(
            below_frame,
            text="Add",
            width=150,
            height=40,
            fg_color="#4caf50",
            text_color="#ffffff",
            font=("Arial", 18, "bold")
        )
        add_button.pack(side="right", 
                        padx=30, 
                        pady=30)

#Temporary display
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add Staff")
    frame = AddStaffFrame(master=root)
    frame.pack(fill="both", expand=True)
    root.configure(bg="#f0f0f0")
    root.mainloop()