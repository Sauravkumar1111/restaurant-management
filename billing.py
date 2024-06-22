import pyrebase
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_pdf(bill_data):
    pdf_filename = "bills.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Define the header
    header = "Bill Details\n\n"

    # Write the header to the PDF
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(header)
    c.drawCentredString((letter[0]-text_width)/2, 750, header)

    # Write bill details to the PDF
    y = 700
    for data in bill_data:
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Order ID: {data[0]}")
        c.drawString(50, y-20, f"Table Number: {data[1]}")
        c.drawString(50, y-40, f"Date & Time: {data[2]}")
        c.drawString(50, y-60, "Items:")
        items = data[3].split("\n")
        for item in items:
            y -= 20
            c.drawString(70, y-60, item)
        y -= 80

    c.save()

    messagebox.showinfo("PDF Generated", f"PDF saved as {pdf_filename}")


def generate_bill():
    # Firebase configuration
    firebaseConfig = {
        "apiKey": "AIzaSyDzKVqAU6zeIsvCLJwuvwOBgdQTDA2GrSY",
        "authDomain": "robot-f8bed.firebaseapp.com",
        "databaseURL": "https://robot-f8bed-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "robot-f8bed",
        "storageBucket": "robot-f8bed.appspot.com",
        "messagingSenderId": "104195790186",
        "appId": "1:104195790186:web:bc44d6ff21d44999a24113",
        "measurementId": "G-S18XRG7MP8"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    # Fetch delivered orders from Firebase
    delivered_orders_ref = db.child("billing_orders").get()

    # Initialize an empty list to store food IDs
    bill_data = []

    # Format the delivered orders into a bill
    if delivered_orders_ref.each() is not None:
        for order in delivered_orders_ref.each():
            food_id = order.val().get("order_id")
            if food_id is not None:
                table_number = order.val()["table_number"]
                selected_items = order.val()["selected_items"]
                datetime_value = order.val()["datetime"]

                # Add data to the bill data list
                bill_data.append((food_id, table_number, datetime_value, "\n".join(selected_items)))
            else:
                print("Food ID not found in order:", order.key())

    return bill_data


def save_bill_to_file(bill_data):
    with open("bill.txt", "w") as file:
        file.write("----- Bill -----\n")
        for data in bill_data:
            file.write(f"Order ID: {data[0]}\n")
            file.write(f"Table Number: {data[1]}\n")
            file.write(f"Date & Time: {data[2]}\n")
            file.write("Items:\n")
            file.write(f"{data[3]}\n")
            file.write("-----------------\n")


def show_bill_details(bill_data):
    # Create a new Tkinter window for displaying bill details
    bill_window = tk.Toplevel()
    bill_window.title("Bill Details")

    bill_content = tk.Text(bill_window)
    bill_content.pack()

    # Insert bill details into the text widget
    bill_content.insert(tk.END, "----- Bill -----\n")
    for data in bill_data:
        bill_content.insert(tk.END, f"Order ID: {data[0]}\n")
        bill_content.insert(tk.END, f"Table Number: {data[1]}\n")
        bill_content.insert(tk.END, f"Date & Time: {data[2]}\n")
        bill_content.insert(tk.END, "Items:\n")
        bill_content.insert(tk.END, f"{data[3]}\n")
        bill_content.insert(tk.END, "-----------------\n")

    bill_content.config(state=tk.DISABLED)  # Make the text widget read-only


def update_table():
    # Fetch new bill data
    bill_data = generate_bill()

    # Clear existing rows
    for record in tree.get_children():
        tree.delete(record)
    
    # Insert new rows
    for data in bill_data:
        tree.insert("", "end", values=data)

    # Schedule the update after 10 seconds (adjust as needed)
    root.after(10000, update_table)


def generate_pdf_and_show():
    bill_data = generate_bill()
    generate_pdf(bill_data)

def generate_pdf_from_text(invoice_text, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Write the invoice text to the PDF
    c.setFont("Helvetica", 12)
    lines = invoice_text.split("\n")
    y = 750
    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()

    messagebox.showinfo("PDF Generated", f"PDF saved as {pdf_filename}")

def generate_pdf_and_show():
    invoice_text = invoice_textarea.get("1.0", "end-1c")  # Get text from the text area
    if invoice_text:
        # Generate a unique filename for the PDF
        pdf_filename = f"invoice_{len(os.listdir('invoices')) + 1}.pdf"
        generate_pdf_from_text(invoice_text, pdf_filename)
    else:
        messagebox.showwarning("No Invoice", "No invoice to generate PDF from.")
def generate_invoice_text(data):
    # Function to generate invoice text from data
    invoice_text = f"----- Invoice -----\n"
    invoice_text += f"Order ID: {data[0]}\n"
    invoice_text += f"Table Number: {data[1]}\n"
    invoice_text += f"Date & Time: {data[2]}\n"
    invoice_text += "Items:\n"
    invoice_text += f"{data[3]}\n"
    invoice_text += "-----------------\n"
    return invoice_text

def display_invoice(event):
    # Function to display invoice text when a row is double-clicked
    item = tree.selection()[0]
    data = tree.item(item)['values']
    invoice_text = generate_invoice_text(data)
    invoice_textarea.config(state=tk.NORMAL)
    invoice_textarea.delete('1.0', tk.END)
    invoice_textarea.insert(tk.END, invoice_text)
    invoice_textarea.config(state=tk.DISABLED)

    # Highlight the selected row
    tree.tag_configure("selected", background="brown")
    tree.tag_remove("selected", "all")
    tree.tag_add("selected", item)


if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Bill Generator")

    # Set the background color to brown
    root.configure(bg="brown")

    # Create a table
    tree = ttk.Treeview(root, columns=("Order ID", "Table Number", "Date & Time", "Items"), show="headings")
    tree.heading("Order ID", text="Order ID")
    tree.heading("Table Number", text="Table Number")
    tree.heading("Date & Time", text="Date & Time")
    tree.heading("Items", text="Items")
    tree.pack(padx=10, pady=10)

    # Double click event to display invoice text
    tree.bind("<Double-1>", display_invoice)

    # Create a text area for displaying invoice text
    invoice_textarea = tk.Text(root, height=10, width=50)
    invoice_textarea.pack(padx=10, pady=10)
    invoice_textarea.config(state=tk.DISABLED)

    # Create a button to generate PDF from the displayed invoice
    generate_pdf_button = tk.Button(root, text="Generate PDF from Invoice", command=generate_pdf_and_show)
    generate_pdf_button.pack(pady=10)

    # Initial update of the table
    update_table()

    # Run the Tkinter event loop
    root.mainloop()
