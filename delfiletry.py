import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

# Global variable to keep track of food ID
food_id_counter = 1

def update_treeview():
    global food_id_counter
    
    # Clear existing data
    pending_tree.delete(*pending_tree.get_children())
    delivered_tree.delete(*delivered_tree.get_children())

    try:
        # Fetch data from Firebase for pending orders
        orders_ref = db.reference("orders").get()
        

        
        if orders_ref is not None:
            for order_key, order_value in orders_ref.items():
                table_number = order_value.get('table_number', '')
                selected_items = order_value.get('selected_items', [])
                datetime_value = order_value.get('datetime', '')
                food_id = order_value.get('order_id', '')
                tag = 'even' if food_id_counter % 2 == 0 else 'odd'
                pending_tree.insert('', tk.END, values=(order_key,food_id, table_number, datetime_value, ", ".join(selected_items)), tags=(tag,))
                food_id_counter += 1

        # Apply alternate row colors to pending_tree
        pending_tree.tag_configure('even', background='#ffcc99')  # Orange color
        pending_tree.tag_configure('odd', background='#ffffff')

        # Fetch data from Firebase for delivered orders
        delivered_orders_ref = db.reference("delivered_orders").get()

        if delivered_orders_ref is not None:
            # Reset food_id_counter before populating delivered orders
            food_id_counter = 1
            for order_key, order_value in delivered_orders_ref.items():
                table_number = order_value.get('table_number', '')
                selected_items = order_value.get('selected_items', [])
                datetime_value = order_value.get('datetime', '')
                food_id = order_value.get('order_id', '')

                tag = 'even' if food_id_counter % 2 == 0 else 'odd'
                delivered_tree.insert('', tk.END, values=(order_key, food_id, table_number, datetime_value, selected_items), tags=(tag,))

                food_id_counter += 1


        # Apply alternate row colors to delivered_tree
        delivered_tree.tag_configure('even', background='#ffcc99')  # Orange color
        delivered_tree.tag_configure('odd', background='#ffffff')

    except Exception as e:
        print("Error:", e)

    root.after(1000, update_treeview)


def move_to_delivered(event):
    try:
        selected_item = pending_tree.selection()[0]
        values = pending_tree.item(selected_item, 'values')

        # Extract the order ID from the values
        order_id = values[0]

        # Delete the selected item from the pending orders in the database
        db.reference("orders").child(order_id).delete()

        # Insert the selected item into the delivered orders in the database with the same format
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"order_id": values[1], "table_number": values[2], "selected_items": values[4].split(", "), "datetime": current_datetime}
        db.reference("delivered_orders").push(data)
        db.reference("billing_orders").push(data)
        # Update the GUI
        update_treeview()

    except IndexError:
        pass


def push_delivered_order_to_billing(event):
    try:
        if not delivered_tree.selection():
            return

        selected_item = delivered_tree.selection()[0]
        values = delivered_tree.item(selected_item, 'values')

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"order_id": values[1], "table_number": values[2], "selected_items": values[4].split(", "), "datetime": current_datetime}
        
        # Push data to billing orders section
        db.reference("billing_orders").push(data)
        
        # Delete the selected item from the delivered orders section
        db.reference("delivered_orders").child(selected_item).delete()

        # Update the GUI
        update_treeview()

    except IndexError:
        pass


root = tk.Tk()
root.title("Order Management System")
root.configure(bg="brown")

# Load and resize the image
image = Image.open("/home/ras2024/Downloads/shaswat/shaswat/assets/logo.png")
image = image.resize((100, 100))
shaswat_logo = ImageTk.PhotoImage(image)

# Common Frame for Labels
label_frame = tk.Frame(root, bg="brown")
label_frame.pack(side=tk.TOP, padx=20, pady=5, fill=tk.X)

# Shaswat Restaurant Label with Image
shaswat_label = tk.Label(label_frame, bg="brown", image=shaswat_logo)
shaswat_label.grid(row=0, column=0, padx=(10, 50), pady=5)

# Shaswat Restaurant Label
shaswat_label = tk.Label(label_frame, bg="brown", text="Shashwat Restaurant", fg="white", font=("cursive", 20))
shaswat_label.grid(row=0, column=1, padx=(5, 50), pady=5)

# Pending Order Label
pending_label = tk.Label(root, text="Pending Orders", bg="brown", fg="white", font=("Bold", 20))
pending_label.pack(side=tk.TOP, padx=20, pady=0, fill=tk.X)

# Frame for pending orders
pending_frame = tk.Frame(root)
pending_frame.pack(side=tk.TOP, padx=20, pady=0, fill=tk.BOTH, expand=True)

# Create a Treeview widget for pending orders
pending_tree = ttk.Treeview(pending_frame, columns=('Unique ID','Order ID', 'Table Number', 'Date', 'Food Item'), show='headings')
pending_tree.heading('Unique ID', text='Unique ID')
pending_tree.heading('Order ID', text='Order ID')
pending_tree.heading('Table Number', text='Table Number')
pending_tree.heading('Date', text='Date')
pending_tree.heading('Food Item', text='Food Item')
pending_tree.column('Unique ID', width=50)
pending_tree.column('Order ID', width=50)
pending_tree.column('Table Number', width=30)
pending_tree.column('Date', width=50)
pending_tree.column('Food Item', width=300)
pending_scrollbar = ttk.Scrollbar(pending_frame, orient="vertical", command=pending_tree.yview)
pending_tree.configure(yscrollcommand=pending_scrollbar.set)
pending_tree.pack(side="left", fill="both", expand=True)
pending_scrollbar.pack(side="right", fill="y")
pending_scrollbar.pack(side="right", fill="y")
pending_tree.pack(side="left", fill="both", expand=True)
pending_tree.bind("<Double-1>", move_to_delivered)

# Delivered Order Label
delivered_label = tk.Label(root, text="Delivered Orders", bg="brown", fg="white", font=("Bold", 20))
delivered_label.pack(side=tk.TOP, padx=20, pady=5, fill=tk.X)

# Frame for delivered orders
delivered_frame = tk.Frame(root)
delivered_frame.pack(side=tk.TOP, padx=20, pady=20, fill=tk.BOTH, expand=True)

delivered_tree = ttk.Treeview(delivered_frame, columns=('Unique ID','Order ID', 'Table Number', 'Date', 'Food Item'), show='headings')
delivered_tree.heading('Unique ID', text='Unique ID')
delivered_tree.heading('Order ID', text='Order ID')
delivered_tree.heading('Table Number', text='Table Number')
delivered_tree.heading('Date', text='Date')
delivered_tree.heading('Food Item', text='Food Item')
delivered_tree.column('Unique ID', width=50)
delivered_tree.column('Order ID', width=50)
delivered_tree.column('Table Number', width=50)
delivered_tree.column('Date', width=150)
delivered_tree.column('Food Item', width=300)
delivered_tree.pack(fill='both', expand=True)


delivered_tree.bind("<Double-1>", push_delivered_order_to_billing)

# Firebase configuration
cred = credentials.Certificate("/home/ras2024/Downloads/shaswat/shaswat/robot-f8bed-firebase-adminsdk-b95ir-6995cec5a4.json")  # Path to your Firebase service account key
firebase_admin.initialize_app(cred, {'databaseURL': 'https://robot-f8bed-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# Call the update_treeview function to initially populate the treeviews
update_treeview()

# Start the Tkinter event loop
root.mainloop()
