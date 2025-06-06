import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# Main window
root = tk.Tk()
root.title("Billing & Payment")
root.geometry("800x500")

# Sample data for billing history
billing_data = []

# Main content area
main_frame = tk.Frame(root, bg="#F5F5F5")
main_frame.pack(fill="both", expand=True)

# Billing History
billing_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
billing_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

billing_label = tk.Label(billing_frame, text="Billing History", font=("Arial", 12, "bold"), bg="#FFFFFF")
billing_label.pack(anchor="w", padx=10, pady=5)

# Billing history table
columns = ("Invoice No.", "Guest Name", "Room Type", "Nights", "Amount", "Status", "Action")
tree = ttk.Treeview(billing_frame, columns=columns, show="headings", height=5)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=80)

# Populate billing history
def populate_billing_history():
    for item in tree.get_children():
        tree.delete(item)
    for data in billing_data:
        invoice_no, guest_name, room_type, nights, amount, status = data
        tree.insert("", "end", values=(invoice_no, guest_name, room_type, nights, f"${amount:.2f}", status, "Update Status"))

populate_billing_history()
tree.pack(fill="both", padx=10, pady=5)

# Update status function
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

# Invoice Generation
invoice_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="raised", bd=1)
invoice_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

invoice_label = tk.Label(invoice_frame, text="Invoice Generation", font=("Arial", 12, "bold"), bg="#FFFFFF")
invoice_label.pack(anchor="w", padx=10, pady=5)

# Invoice details
invoice_number = "INV505"
tk.Label(invoice_frame, text=f"INVOICE {invoice_number}", font=("Arial", 10), bg="#FFFFFF").pack(anchor="w", padx=10)

# Guest Info
guest_frame = tk.Frame(invoice_frame, bg="#FFFFFF")
guest_frame.pack(fill="x", padx=10)
tk.Label(guest_frame, text="GUEST INFORMATION", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w")

name_label = tk.Label(guest_frame, text="Name:", bg="#FFFFFF")
name_label.pack(anchor="w")
name_entry = tk.Entry(guest_frame)
name_entry.pack(anchor="w")
name_entry.insert(0, "Emily Johnson")

address_label = tk.Label(guest_frame, text="Address:", bg="#FFFFFF")
address_label.pack(anchor="w")
address_entry = tk.Entry(guest_frame)
address_entry.pack(anchor="w")
address_entry.insert(0, "456 Pine Road, Seattle, WA 98101")

contact_label = tk.Label(guest_frame, text="Contact Number:", bg="#FFFFFF")
contact_label.pack(anchor="w")
contact_entry = tk.Entry(guest_frame)
contact_entry.pack(anchor="w")
contact_entry.insert(0, "+1 (206) 555-7890")

# Booking Info
booking_frame = tk.Frame(invoice_frame, bg="#FFFFFF")
booking_frame.pack(fill="x", padx=10, pady=5)
tk.Label(booking_frame, text="BOOKING INFORMATION", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w")

check_in_label = tk.Label(booking_frame, text="Check in (YYYY-MM-DD):", bg="#FFFFFF")
check_in_label.pack(anchor="w")
check_in_entry = tk.Entry(booking_frame)
check_in_entry.pack(anchor="w")
check_in_entry.insert(0, "2025-06-10")

check_out_label = tk.Label(booking_frame, text="Check out (YYYY-MM-DD):", bg="#FFFFFF")
check_out_label.pack(anchor="w")
check_out_entry = tk.Entry(booking_frame)
check_out_entry.pack(anchor="w")
check_out_entry.insert(0, "2025-06-15")

guests_label = tk.Label(booking_frame, text="Guests:", bg="#FFFFFF")
guests_label.pack(anchor="w")
guests_entry = tk.Entry(booking_frame)
guests_entry.pack(anchor="w")
guests_entry.insert(0, "3")

room_type_label = tk.Label(booking_frame, text="Room Type:", bg="#FFFFFF")
room_type_label.pack(anchor="w")
room_type_entry = tk.Entry(booking_frame)
room_type_entry.pack(anchor="w")
room_type_entry.insert(0, "Deluxe Suite")

# Payment Breakdown Table
payment_label = tk.Label(invoice_frame, text="PAYMENT BREAKDOWN", font=("Arial", 10, "bold"), bg="#FFFFFF")
payment_label.pack(anchor="w", padx=10)

payment_columns = ("Service Description", "Subtotal", "Tax", "Total")
payment_tree = ttk.Treeview(invoice_frame, columns=payment_columns, show="headings", height=3)

for col in payment_columns:
    payment_tree.heading(col, text=col)
    payment_tree.column(col, width=80)

# Payment entry fields
payment_entry_frame = tk.Frame(invoice_frame, bg="#FFFFFF")
payment_entry_frame.pack(fill="x", padx=10, pady=5)

service_label = tk.Label(payment_entry_frame, text="Service Description:", bg="#FFFFFF")
service_label.pack(anchor="w")
service_entry = tk.Entry(payment_entry_frame)
service_entry.pack(anchor="w")
service_entry.insert(0, "Room Charge")

subtotal_label = tk.Label(payment_entry_frame, text="Subtotal:", bg="#FFFFFF")
subtotal_label.pack(anchor="w")
subtotal_entry = tk.Entry(payment_entry_frame)
subtotal_entry.pack(anchor="w")
subtotal_entry.insert(0, "750.00")

tax_label = tk.Label(payment_entry_frame, text="Tax:", bg="#FFFFFF")
tax_label.pack(anchor="w")
tax_entry = tk.Entry(payment_entry_frame)
tax_entry.pack(anchor="w")
tax_entry.insert(0, "75.00")

# List to store payment data
payment_data = []

# Populate payment breakdown
def populate_payment_breakdown():
    for item in payment_tree.get_children():
        payment_tree.delete(item)
    for data in payment_data:
        payment_tree.insert("", "end", values=data)

# Add payment entry
def add_payment():
    service = service_entry.get()
    try:
        subtotal = float(subtotal_entry.get())
        tax = float(tax_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Subtotal and Tax must be numbers")
        return

    total = subtotal + tax
    payment_data.append((service, subtotal, tax, total))
    populate_payment_breakdown()
    service_entry.delete(0, tk.END)
    subtotal_entry.delete(0, tk.END)
    tax_entry.delete(0, tk.END)
    update_totals()

# Pre-fill payment data
def prefill_payment():
    service = service_entry.get()
    subtotal = float(subtotal_entry.get())
    tax = float(tax_entry.get())
    total = subtotal + tax
    payment_data.append((service, subtotal, tax, total))
    populate_payment_breakdown()

prefill_payment()
payment_tree.pack(fill="x", padx=10)

# Add payment button
tk.Button(payment_entry_frame, text="Add Payment", bg="#4A90E2", fg="white", command=add_payment).pack(anchor="w", pady=5)

# Grand Total and Downpayment
grand_total_label = tk.Label(invoice_frame, text="Grand Total: $0.00", font=("Arial", 10, "bold"), bg="#FFFFFF")
grand_total_label.pack(anchor="w", padx=10)
downpayment_label = tk.Label(invoice_frame, text="Downpayment: $0.00", bg="#FFFFFF")
downpayment_label.pack(anchor="w", padx=10)

# Update totals
def update_totals():
    grand_total = sum(item[3] for item in payment_data)
    downpayment = grand_total * 0.3  # 30% downpayment
    grand_total_label.config(text=f"Grand Total: ${grand_total:.2f}")
    downpayment_label.config(text=f"Downpayment: ${downpayment:.2f}")
    return grand_total

update_totals()

# Additional Information
tk.Label(invoice_frame, text="ADDITIONAL INFORMATION", bg="#FFFFFF", justify="left").pack(anchor="w", padx=10, pady=5)
additional_info = tk.Text(invoice_frame, height=3, width=40)
additional_info.pack(anchor="w", padx=10)
additional_info.insert("end", "Payment due within 7 days.\nContact us for any queries.\nThank you for your business!")

# Button functions
def generate_invoice():
    name = name_entry.get()
    room_type = room_type_entry.get()
    try:
        nights = int((datetime.strptime(check_out_entry.get(), "%Y-%m-%d") - datetime.strptime(check_in_entry.get(), "%Y-%m-%d")).days)
        if nights <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid date format or number of nights")
        return

    if not name or not room_type:
        messagebox.showerror("Error", "Name and Room Type are required")
        return

    new_invoice_number = f"INV{random.randint(100, 999)}"  # Generate new invoice number
    grand_total = update_totals()
    new_invoice = (
        new_invoice_number,
        name,
        room_type,
        nights,
        grand_total,
        "Pending"
    )
    billing_data.append(new_invoice)
    populate_billing_history()
    messagebox.showinfo("Success", f"Invoice {new_invoice_number} generated successfully!")

def send_invoice_email():
    if not billing_data:
        messagebox.showerror("Error", "No invoice to send")
        return
    messagebox.showinfo("Email", "Invoice email sent to customer!")

# Buttons
button_frame = tk.Frame(invoice_frame, bg="#FFFFFF")
button_frame.pack(fill="x", padx=10, pady=5)
tk.Button(button_frame, text="Generate Invoice", bg="#4A90E2", fg="white", command=generate_invoice).pack(side="right", padx=5)
tk.Button(button_frame, text="Invoice Email", relief="flat", command=send_invoice_email).pack(side="right", padx=5)

root.mainloop()