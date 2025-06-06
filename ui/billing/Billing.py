import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import random

#Notes ni Sofia: 
#1. Update button leads to a pop-up window where employee
# can update billing information.
#2. View invoice button leads to the billing breakdown GUI.
#The UI dapat ng breakdown is ilalagay ko nalang sa billing breakdown GUI.
#Magiging double kasi if may create din dito, sa create reservation dapat mag ppull ng info
#--------------------------------------------------------------#
# Problems encountered:
# 1. The button to view invoice information is not displaying properly on top of the treeview.
# 2. The categories in the treeview are not aligning properly to the left.

ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Billing & Payment")
root.geometry("1600x800")

billing_data = []

main_frame = ctk.CTkFrame(root, fg_color="#F5F5F5")
main_frame.pack(fill="both", expand=True)

billing_frame = ctk.CTkFrame(main_frame, fg_color="transparent", 
                             )
billing_frame.pack(side="left", 
                   fill="both", 
                   expand=True, 
                   padx=10, 
                   pady=20)

billing_label = ctk.CTkLabel(billing_frame,
                             text="Billing History",
                             font=("Arial", 20, "bold"),
                             text_color="#222")
billing_label.pack(anchor="w", padx=10, pady=10)

#Billing History list
columns = ("Invoice No.", "Guest Name", "Nights", "Amount", "Status")

#I can't display categories to the left for some reason, it ruins the pop up 
# on the invoice information frame - Sofia
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 15, "bold"), anchor="w")
style.configure("Treeview", rowheight=35)
style.layout("Treeview", [
    ('Treeview.treearea', {'sticky': 'nswe'})
])
style.configure("Treeview", font=("Arial", 15))
tree = ttk.Treeview(billing_frame, columns=columns, show="headings", height=5)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=90)
tree.pack(fill="both", padx=10, pady=5)

# Add placeholder billing data
billing_data = [
    (f"INV{1000+i}", f"Guest {i+1}", "Deluxe", random.randint(1, 5), random.randint(2000, 8000), random.choice(["Pending", "Paid"]))
    for i in range(5)
]

def show_invoice_frame(event=None):
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No selection", "Please select an invoice to view.")
        return
    values = tree.item(selected, "values")
    if not values:
        messagebox.showwarning("No selection", "Please select an invoice to view.")
        return
    for data in billing_data:
        if str(data[0]) == str(values[0]):
            fill_invoice_fields(data)
            break
    invoice_frame.pack(side="right", fill="y", padx=10, pady=20)

# Button is having trouble moving on top of the treeview
button_above_tree_frame = ctk.CTkFrame(billing_frame, fg_color="transparent")
button_above_tree_frame.pack(fill="x", padx=10, pady=(0, 5))

view_invoice_btn = ctk.CTkButton(
    button_above_tree_frame,
    text="View Invoice Information",
    fg_color="#4A90E2",
    text_color="white",
    font=("Arial", 16, "bold"),
    command=show_invoice_frame
)
view_invoice_btn.pack(anchor="nw", padx=10, pady=5)


#Logic for list *Can be changed if needed
def populate_billing_history():
    for item in tree.get_children():
        tree.delete(item)
    for data in billing_data:
        invoice_no, guest_name, room_type, nights, amount, status = data
        tree.insert("", "end", values=(invoice_no, guest_name, room_type, nights, f"${amount:.2f}", status, "Update Status"))

populate_billing_history()

def update_status(event):
    item = tree.identify_row(event.y)
    if item:
        index = tree.index(item)
        if 0 <= index < len(billing_data):
            current_status = billing_data[index][5]
            new_status = "Paid" if current_status == "Pending" else "Pending"
            billing_data[index] = billing_data[index][:5] + (new_status,)
            populate_billing_history()
            messagebox.showinfo("Success", f"Status updated to {new_status}")

tree.bind("<Double-1>", update_status)

#Invoice information frame 

invoice_frame = ctk.CTkFrame(main_frame, 
                             fg_color="#FFFFFF", 
                             border_width=1, 
                             border_color="#CCCCCC")

#Label
# Close button for Invoice Information frame
def close_invoice_frame():
    invoice_frame.pack_forget()

# Create a frame to hold the invoice label and close button side by side
invoice_header_frame = ctk.CTkFrame(invoice_frame, fg_color="transparent",)
invoice_header_frame.pack(fill="x", padx=10, pady=(10, 10))

invoice_label = ctk.CTkLabel(invoice_header_frame, text="Invoice Information",
                             font=("Arial", 20, "bold"), 
                             text_color="#222")
invoice_label.pack(side="left", anchor="w", padx=20, pady=(0,5))

close_btn = ctk.CTkButton(
    invoice_header_frame,
    text="X",
    fg_color="#E74C3C",
    text_color="white",
    font=("Arial", 12, "bold"),
    width=30,
    height=25,
    command=close_invoice_frame
)
close_btn.pack(side="right", anchor="e", padx=10, pady=5)

selected_invoice_number = ctk.CTkLabel(invoice_frame, text="Invoice No: -",
                                       font=("Arial", 16), 
                                       text_color="#333")
selected_invoice_number.pack(anchor="w", padx=20)

# Guest and Booking Information
guest_frame = ctk.CTkFrame(invoice_frame, 
                           fg_color="#FFFFFF")
guest_frame.pack(fill="x", padx=20)
ctk.CTkLabel(guest_frame, text="Guest Information", 
             font=("Arial", 18, "bold")).pack(anchor="w")

name_address_frame = ctk.CTkFrame(guest_frame, fg_color="#FFFFFF")
name_address_frame.pack(fill="x")

name_label = ctk.CTkLabel(name_address_frame,
                          text="Name:",
                          font=("Arial", 16))
name_label.pack(side="left", padx=(20, 5))
name_entry = ctk.CTkEntry(name_address_frame, width=120)
name_entry.pack(side="left")

# Create a new frame for address below the name/address frame
address_frame = ctk.CTkFrame(guest_frame, fg_color="#FFFFFF")
address_frame.pack(fill="x")

address_label = ctk.CTkLabel(address_frame,
                             text="Address:",
                             font=("Arial", 16))
address_label.pack(side="left", padx=(20, 5), pady=(10, 0))
address_entry = ctk.CTkEntry(address_frame, width=230)
address_entry.pack(side="left", pady=(10, 0))

contact_label = ctk.CTkLabel(name_address_frame,
                             text="Contact:",
                             font=("Arial", 16))
contact_label.pack(side="left", padx=(20, 5))
contact_entry = ctk.CTkEntry(name_address_frame,
                             width=150)
contact_entry.pack(side="left", padx=(0, 20))

email_label = ctk.CTkLabel(name_address_frame,
                           text="Email:",
                           font=("Arial", 16))
email_label.pack(side="left", padx=(20, 5))
email_entry = ctk.CTkEntry(name_address_frame, width=180)
email_entry.pack(side="left", padx=(0, 20))


booking_frame = ctk.CTkFrame(invoice_frame,
                             fg_color="#FFFFFF")
booking_frame.pack(fill="x", padx=20, pady=(20,10))
ctk.CTkLabel(booking_frame, text="Booking Information",
             font=("Arial", 18, "bold")).pack(anchor="w")

check_in_out_frame = ctk.CTkFrame(booking_frame, fg_color="#FFFFFF")
check_in_out_frame.pack(fill="x")

check_in_label = ctk.CTkLabel(check_in_out_frame,
                              text="Check in (YYYY-MM-DD):",
                              font=("Arial", 16))
check_in_label.pack(side="left",padx=(20, 5))
check_in_entry = ctk.CTkEntry(check_in_out_frame, width=120)
check_in_entry.pack(side="left", padx=(20, 20))

check_out_label = ctk.CTkLabel(check_in_out_frame,
                               text="Check out (YYYY-MM-DD):",
                               font=("Arial", 16))
check_out_label.pack(side="left")
check_out_entry = ctk.CTkEntry(check_in_out_frame, width=120)
check_out_entry.pack(side="left", padx=5)

guests_roomtype_frame = ctk.CTkFrame(booking_frame, fg_color="#FFFFFF")
guests_roomtype_frame.pack(fill="x", pady=10)

guests_label = ctk.CTkLabel(guests_roomtype_frame,
                            text="Guests:", font=("Arial", 16))
guests_label.pack(side="left", padx=(20, 5))
guests_entry = ctk.CTkEntry(guests_roomtype_frame, width=80)
guests_entry.pack(side="left")

room_type_label = ctk.CTkLabel(guests_roomtype_frame,
                               text="Room Type:",
                               font=("Arial", 16))
room_type_label.pack(side="left", padx=(15, 5))
room_type_entry = ctk.CTkEntry(guests_roomtype_frame, width=120)
room_type_entry.pack(side="left")

payment_label = ctk.CTkLabel(invoice_frame,
                             text="Payment Details",
                             font=("Arial", 18, "bold"),
                             padx=20, pady=10)
payment_label.pack(anchor="w", padx=10)


ctk.CTkLabel(invoice_frame, text="Additional Information", anchor="w", 
             font=("Arial", 18)).pack(anchor="w", padx=20, pady=(20,10))
additional_info = ctk.CTkTextbox(invoice_frame, height=60, width=500)
additional_info.pack(anchor="w", padx=10)
additional_info.insert("end", "Payment due within 7 days.Contact us for any queries.Thank you for your business!")

# Sample billing data *Not sure, can be deleted - Sofia
def fill_invoice_fields(data):
    invoice_no, guest_name, room_type, nights, amount, status = data
    selected_invoice_number.configure(text=f"INVOICE: {invoice_no}")
    name_entry.delete(0, "end")
    name_entry.insert(0, guest_name)
    address_entry.delete(0, "end")
    contact_entry.delete(0, "end")
    room_type_entry.delete(0, "end")
    room_type_entry.insert(0, room_type)
    try:
        check_in = datetime.today()
        check_out = check_in.replace(day=check_in.day + int(nights))
        check_in_entry.insert(0, check_in.strftime("%Y-%m-%d"))
        check_out_entry.insert(0, check_out.strftime("%Y-%m-%d"))
    except Exception:
        check_in_entry.insert(0, "")
        check_out_entry.insert(0, "")
    guests_entry.delete(0, "end")
    guests_entry.insert(0, "1")
    global payment_data
    payment_data = []
    #populate_payment_breakdown()
   # update_totals()
    additional_info.delete("1.0", "end")
    additional_info.insert("end", "Payment due within 7 days.\nContact us for any queries.\nThank you for your business!")

def on_tree_select(event):
    item = tree.focus()
    if item:
        values = tree.item(item, "values")
        if values:
            for data in billing_data:
                if str(data[0]) == str(values[0]):
                    fill_invoice_fields(data)
                    break

tree.bind("<<TreeviewSelect>>", on_tree_select)

def update_billing():
    # Get the currently selected item's values from the treeview
    item = tree.focus()
    if not item:
        messagebox.showerror("Error", "No invoice selected to update")
        return
    values = tree.item(item, "values")
    if not values:
        messagebox.showerror("Error", "No invoice selected to update")
        return

    # Pop up window for editing billing info
    popup = ctk.CTkToplevel(root)
    popup.title("Update Billing")
    popup.geometry("400x350")

    ctk.CTkLabel(popup, text="Update Billing Information", font=("Arial", 18, "bold")).pack(pady=10)

    # Payment Status
    ctk.CTkLabel(popup, text="Status:").pack(anchor="w", padx=20)
    status_var = ctk.StringVar(value=values[5])
    status_combo = ctk.CTkComboBox(popup, values=["Pending", "Paid"], variable=status_var)
    status_combo.pack(fill="x", padx=20, pady=2)

    # Total Amount Paid
    ctk.CTkLabel(popup, text="Total Amount Paid:").pack(anchor="w", padx=20, pady=(10, 0))
    total_paid_var = ctk.StringVar(value=str(values[4]) if status_var.get() == "Paid" else "0.00")
    total_paid_entry = ctk.CTkEntry(popup, textvariable=total_paid_var, state="readonly")
    total_paid_entry.pack(fill="x", padx=20, pady=2)

    def on_status_change(event=None):
        if status_var.get() == "Paid":
            total_paid_var.set(str(values[4]))
        else:
            total_paid_var.set("0.00")
    status_combo.bind("<<ComboboxSelected>>", on_status_change)

    def save_update():
        item = tree.focus()
        if not item:
            messagebox.showerror("Error", "No invoice selected to update")
            return
        values = tree.item(item, "values")
        if not values:
            messagebox.showerror("Error", "No invoice selected to update")
            return
        for idx, data in enumerate(billing_data):
            if str(data[0]) == str(values[0]):
                billing_data[idx] = (
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    float(values[4].replace("$", "")),
                    status_var.get()
                )
                break
        populate_billing_history()
        popup.destroy()
        messagebox.showinfo("Success", "Billing updated successfully!")

    ctk.CTkButton(popup, text="Save", command=save_update).pack(pady=15)
    ctk.CTkButton(popup, text="Cancel", fg_color="#888", command=popup.destroy).pack()

#View Invoice leads to the billing breakdown GUI

button_frame = ctk.CTkFrame(invoice_frame, fg_color="#FFFFFF")
button_frame.pack(fill="x", padx=10, pady=5)
ctk.CTkButton(button_frame, text="View Invoice", fg_color="#4A90E2",
              text_color="white",
              font=("Arial", 16, "bold")).pack(side="right", padx=5)
ctk.CTkButton(button_frame, text="Update Billing", fg_color="#27AE60",
              text_color="white",
              font=("Arial", 16, "bold"),
              command=update_billing).pack(side="right", padx=5)

root.mainloop()
