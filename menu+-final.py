import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, db
import datetime                                                               
import os
from tkinter import font
import pyttsx3

class WaiterMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Waiter Menu")
        self.selected_items = {}
        cred = credentials.Certificate("/home/ras2024/Downloads/shaswat/shaswat/robot-f8bed-firebase-adminsdk-b95ir-6995cec5a4.json")  # Path to your Firebase service account key
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://robot-f8bed-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        self.db = db.reference('')
        # Make the window fullscreen
        #self.attributes('-fullscreen', True)

        # Load and resize logo image
        self.logo_image = tk.PhotoImage(file="/home/ras2024/Downloads/shaswat/shaswat/assets/logo.png").subsample(2, 3)  # Adjust subsample parameters as needed

        # Create label for logo
        self.logo_label = tk.Label(self, image=self.logo_image,)
        self.logo_label.place(x=10, y=5)  # Adjust x and y coordinates as needed# Load and resize photo image for top-right corner
        self.photo_image = tk.PhotoImage(file="/home/ras2024/Downloads/shaswat/shaswat/assets/Restaurantjhjh.png").subsample(3, 3)
        
  # Adjust subsample parameters as needed
    
        # Create label for photo at top-right corner
        try:

            self.photo_label = tk.Label(self, image=self.photo_image)
            self.photo_label.place(x=self.winfo_screenwidth() - self.photo_image.width(), y=0)  # Place at top-right corner
        except tk.TclError as e:
            print("Error loading image:", e)

           
        # Firebase configuration


        # Set up table selection
        self.table_label = tk.Label(self, text="Select Table Number:", bg="yellow", font=("Arial", 12, "bold"))
        self.table_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 21)], font=("Arial", 12, "bold"))
        #self.table_combobox.set("1")  # Default to table 1
        #self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm_table)

        self.table_label.pack(pady=10)
        self.table_combobox.pack(pady=5)
        #self.confirm_button.pack(pady=5)

        # Frames for buttons and items
        self.buttons_frame = tk.Frame(self,bg="brown")
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.items_frame = tk.Frame(self)
        self.items_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.items_frame.pack_propagate(0)  # Fix frame size


        self.frames = {}  # Store frames for different sections
        self.create_frames()

        # Frame to display selected items
        self.selected_items_frame = tk.Frame(self, bg="brown")
        self.selected_items_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.selected_items_frame.pack_propagate(0)  # Fix frame size
        self.selected_items_label = tk.Label(self.selected_items_frame, text="Selected Items:", font=("Ubuntu", 14, "bold"))
        self.selected_items_label.pack(pady=5)
        self.selected_items_display = tk.Text(self.selected_items_frame, height=30, width=40)
        self.selected_items_display.pack()
        
        # Confirm Order button
        self.confirm_order_button = tk.Button(self.selected_items_frame, text="Confirm Order", command=self.confirm_order,font=("Ubuntu", 14, "bold") )
        self.confirm_order_button.pack(pady=10)

    def create_frames(self):
        # Define food items for different sections
        food_items = {
            "Chinese Rice": [
                "VEG FRIED RICE- 160/-",
"VEG SCHEZUAN FRIED RICE- 165/-",
"MEXICAN FRIED RICE- 180/-", 
"VEG HAKKA NOODLES- 140/-",
"VEG SCHEZUAN NOODLES- 160/-",
"PICLE RICE WITH NOODLE- 180/-",
"CHINESE COMBO- 240/-",
"MANCHOW NOODLES GRAVY- 195/-",
"PANEER CHOWMEIN- 220"
],


            "Sweets": [
                "RASMALAI (2Pcs)",
                "GULAB JAMUN(4Pcs)",
                "RAJ BHOG(2Pcs)",
                "Fruit Salad",
                "FRUIT SALAD WITH ICE CREAME",
                "RASGULLA",
                "SEASONAL SWEETS",
                "CHEENA PIECE"],

            "Fast Food": [
                "CHOOLA BHATURA(2PC)- 100/-",
                "EXTRA BHATURA- 40/-"
                "SPL. DAHIBARA/BHALLA- 80/-",
                "GOL GAPPA(6PC)- 40/-",
                "GOL GAPPA CHAT- 40/-",
                "PAPRI CHAAT- 100/-",
                "PAV BHAJI -110/-"
],

                     

                 "Indian Vegetable":[
                    "MIX VEG- 240/-",
"VEG KOLHAPURI- 255/-",
"VEG HANDI- 255/-",
"VEG HARIYALI- 270/-",
"VEG KOFTA CURRY- 270/-",
"MALAI KOFTA- 300/-",
"PALAK KOFTA- 220/-",
"MASHROOM MATAR MASALA- 260/-",
"CORN PALAK LAHSUNIA TADKA- 280/-",
"KASHMIRI METHI CHAMAN- 265/-", 
"CHANA MASALA- 240/-",
"CHULEY PUNJABI- 240/-",
"NAVRATAN KORMA- 300/-",
"KAJU CURRY- 340/-",
"ALOO JEERA- 190/-",
"ALOO DO PYAZA- 220/-",
"ALOO DAM- 220/-",
"SEASONAL VEG- 250/-",
"VEG GAHFREWZI- 240/-",
"KAJU KORMA- 365/-",
"MASHROOM TIKKA MAKHAN MASALA- 320/-",
"SHASHWAT SEP. VEG- 280/-",
"BABYCORN MASALA- 350/-",
"TAWA VEG- 260/-",
"NANHI SABJIYO KA MELA-280/-"
"MASHROOM MASALA- 280/-",
"MASHROOM DO PLAZA- 285/-",
"KAIDHAI MASHROOM- 290/-",
"STUFF TOMATO/CAPSICUM -280/-"],




"Welcome Drink":[
    "JUICE- 110/-",
 "MINERAL WATER-  150/- ",
"COLD COFFEE  200/- ",
"COLD COFEE WITH ICE-CREAME  100/- ",
"SOFT DRINK (300ml)",
"LASSI- 80/-",
"HOT COFFEE- 70"
"HOT TEA- 50/-",
"SHAKE- 140/-",
"SHAKE WITH ICE-CREAME- 160/-",	
"BUTTER MILK- 50/-",
"FRESH LIME SODA- 75/-",
"FRESH LIME WATER- 60/-",
"ICE/LEMON TEA- 80/-",
"MASALA THUMS-UP- 90/-",
"KESAR BADAM MILK- 70/-",
"OREO CHOCOLATE SHAKE- 180/-"
],

"Mocktails":[
    "FRUIT PUNCH- 120/-",
"MOJITO MINT- 120/-",
"DARK SURPRISE- 120/-",
"BLUE LAGOON- 120/-",
"STAWBERRY DÉCOR- 120/-",
"LEMON JACK-120/-",
"MANGO DELIGHT- 120/-",
"LOVER’S DELIGHT-120/-",
"STAWBERRY REFRESHER- 120/-",
"ORANGE MINT REFRESHER- 120/-",
],

"Soup":["TOMATO SOUP- 120/-",
"SWEET CORN SOUP- 125/-",
"MANCHOW SOUP- 110/-",
"HOT AND SOUR SOUP- 140/-",
"MINESTONE SOUP- 110/-",
"LEMON CORRIENDER SOUP- 120/-",
"PALAK SOUP- 120/-",
"VEG CLEAR SOUP- 110/-",
"TOMATO DHANIYA KA SHORBA- 110/-",
"CREAME OF MUSHROOM SOUP- 150/-",
"CHINESE MUSHROOM SOUP- 160"
],

"Khaane ke Saath":[
    "ONION SALAD- 60/- ",
"GREEN SALAD- 80/-",
"RUSSIAN SALAD- 125/-",
"KUKUMBER SALAD- 80/-",
"JAPANESE SALAD- 90/-",
"RAITA- 110/-",
"MIX-VEG RAITA- 110/-",
"PINEAPPLE RAITA- 125/-",
"PAPAD- 20/-",
"MASALA PAPAD- 40/-",
"BUNDI RAITA- 100/-",
"FRUIT SALAD- 125/-",
],

"Chinese Starter":["VEG-MANCHURIAN DRY- 240/-",
"VEG-MANCHURIAN GRAVY-  260/-",
"PANEER CHILLI DRY- 255/-",
"PANEER CHILLI GRAVY- 265/-",
"HONEY CHILLI POTATO- 240/-",
"AMERICAN CORN SALT AND PEPPER- 255/-",
"PANEER 65- 240/-",
"CRISPY VEG- 255/-",
"CHILLI GARLIC POTATO- 240/-",
"CRISPY CHILLI BABYCORN- 255/-",
"MUSHROOM CHILLI DRY- 265/-",
"MUSHROOM CHILLI GRAVY- 275/-",
"SCHEZUAN PANEER- 255/-",
"PANEER MANCHURIAN DRY- 240/-",
"PANEER MANCHURIAN gravy- 240/-",
"LOVELY PANEER- 265/-",
"STICK PANEER- 265/-",
"SPRING ROLL- 200/-",
"CHINESE PLATTER- 300/-",
"MOMO",
"KURKURE MOMO",
"PANEER HOT PAN",
"AMERICAN CHOPEICY",
"CHINESE BHEL",
"VEG-LOLLIPOP",
"GOLDEN FRIED BABYCORN",
"SOYA CHAP",



],
"Tandoori Breads":
[
   "PLAIN ROTI/ BUTTER- 25/ 30",
"NAAN PLAIN /BUTTER- 35/40",
"LACHA PARATHA- 45/-",
"PUDINA PARATHA- 45/-",
"STUFFED KULCHA- 50/-",
"GARLIC NAAN- 70/-",
"STUFFED NAAN- 60/-",
"GARLIC NAAN- 60/-",
"STUFFED KULCHA- 50/-",
"STUFFED PARATHA- 60/-",
"MISSI ROTI- 50/-",
"BUTTER KULCHA- 45/-",
"CHEESE NAAN- 70/-",
"ROTI BASKET- 200/-",
"AALOO PARATHA- 50/-",
"PANEER PARATHA- 60/-",
"KASHMIRI NAAN- 80/-",

],

"DAL AND RICE ":
["PLAIN RICE- 140/-",
"VEG PULAO- 180/-",
"GREEN PEAS PULAO- 170/-",
"KASHMIRI PULAO- 200/-",
"JEERA RICE- 170/-",
"VEG BIRYANI- 240/-"
"VEG-HANDI BIRYANI- 260/-",
"VEG-HYDERABADI BIRYANI- 260/-" ,
"MATKA BIRYANI- 300/-",
"DAL FRY- 180/-",
"DAL TARKA- 195/-",
"DAL MAKHNI- 225/-"
],
"NORTH indian": 
["KADHAI PANEER- 285/-",
    "PANEER BUTTER MASALA- 280/-",
    "PANEER DO PYAJA- 285/- ",
    "PANEER TIKKA MASALA- 285/- ",
    "PANEER LAHSOONIYA TADKA- 285/-",
    "PALAK PANEER- 300/-",
    "PANEER LABBABDAR- 290/-",
    "PANEER MAKHANI- 285/-",
    "SHAHI PANEER- 285/-",
    "PANEER TOOFANI- 310/-",
    "SHASHWAT SPL. PANEER- 310/-",
    "PANEER BHURJI- 280/-",
    "MUTTER PANEER- 280/-",
    "PANEER PASANDA- 320/-",
    "TAWA PANNER- 320/-",
    "MATKA PANEER- 310/-",
    "PANEER PATIYALA- 310/-",
    "MASHROOM PANEER MASALA- 260/-"
    ], 
    "SOUTH INDIAN":
                    [ "IDLI SAMBHAR- 90/- ",
                "PAPER DOSA- 110/-",
                "MASALA DOSA- 120/-",
                "CHEESE MASALA DOSA- 140/-",
                "RAWA PLAIN DOSA- 120/-",
                "PANEER MASALA DOSA- 130/-",
                "BUTTER MASALA DOSA- 150/-",
                "RAWA MASALA DOSA- 145/-",
                "ONION UTTAPAM- 140/-",
                "NO ONION GARLIC MASALA DOSA- 150/-",
                "TOMATO UTTAPAM- 140/-",
                "MIX VEG UTTAPAM-160/-",
                "IDLI SAMBHAR- 90/-",
                "SAMBHAR-150/-"], 

                "ITALIAN":
                ["FRENCH FRIES- 90/-"
                 "PERI PERI FRENCH FRIES- 100/-"
                 "CHEESE FRENCH FRIES - 115/-"
                 "CHEESE GARLIC BRED- 105/-"
                 "FRENCH GRALIC BRED- 80/-"
                 "EXECUTIVE CHEESE GARLIC BRED- 110/-"
                 ""]

            # Add more sections and items here
        }

        for section, items in food_items.items():
            frame = tk.Frame(self.items_frame)
            self.frames[section] = frame
            #category size button inc/dec with their font
            button = tk.Button(self.buttons_frame, text=section, command=lambda sec=section: self.show_section(sec), font=("Ubuntu", 14, "bold"))  
            button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

            if section == "Chinese Rice":  # Check if the section is Chinese Rice
                frame.pack(fill=tk.BOTH, expand=True)  # Show the frame if it's Chinese Rice
            else:
                frame.pack_forget()  # Hide other frames initially
            

            for item in items:
                var = tk.IntVar()
                item_frame = tk.Frame(frame)
                item_frame.pack(anchor="ne")
                item_label = tk.Label(item_frame, text=item, font=("Arial", 10, "bold"))  # Increase font size for items)
                item_label.pack(side=tk.LEFT)
                checkbox = tk.Checkbutton(item_frame, variable=var, command=self.update_selected_items, width=8, height=2)
                checkbox.pack(side=tk.LEFT)

                # Frame to contain the "+" and "-" buttons
                buttons_frame = tk.Frame(item_frame,bg="brown")
                buttons_frame.pack(side=tk.LEFT)

                # Define a font style
                button_font = font.Font(size=12)  # Adjust size as needed
                # Buttons to increase/decrease quantity
                plus_button = tk.Button(buttons_frame, text="+", command=lambda it=item: self.increase_quantity(it),  width=8, height=2, font=button_font)
                plus_button.pack(side=tk.LEFT, padx=(0,5))
                minus_button = tk.Button(buttons_frame, text="-", command=lambda it=item: self.decrease_quantity(it), width=8, height=2, font=button_font)
                minus_button.pack(side=tk.LEFT, padx=(0,5))

                self.selected_items[item] = {"var": var, "quantity": tk.IntVar(value=0)}  # IntVar to store quantity



    def show_section(self, section):
        for sec, frame in self.frames.items():
            if sec == section:
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()

        # Change button color to red when clicked
        for button in self.buttons_frame.winfo_children():
            if button['text'] == section:
                button.config(bg="green")
            else:
                button.config(bg="White")

    def confirm_table(self):
        table_number = self.table_combobox.get()
        selected_items_text = self.order_label.text()
        selected_items = selected_items_text.split('\n')[1:]

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"table_number": table_number, "selected_items": selected_items, "datetime": current_datetime}
        self.db.child("orders").push(data)

        messagebox.showinfo("Confirmation", f"Order for Table {table_number} confirmed.")

        # Clear selected items for next order
        for item_data in self.selected_items.values():
            item_data["var"].set(0)
            item_data["quantity"].set(0)

    def update_selected_items(self):
        selected_items = [item for item, data in self.selected_items.items() if data["var"].get() == 1]
        self.selected_items_display.delete(1.0, tk.END)
        for item in selected_items:
            self.selected_items_display.insert(tk.END, item + " x" + str(self.selected_items[item]["quantity"].get()) + "\n")

    def increase_quantity(self, item):
        self.selected_items[item]["quantity"].set(self.selected_items[item]["quantity"].get() + 1)
        self.update_selected_items()

    def decrease_quantity(self, item):
        quantity = self.selected_items[item]["quantity"].get()
        if quantity > 0:
            self.selected_items[item]["quantity"].set(quantity - 1)
            self.update_selected_items()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def confirm_order(self):
        table_number = self.table_combobox.get()
        selected_items_dict = {}
        index = 0

        # Create an instance of the pyttsx3 engine
        engine = pyttsx3.init()

        # Check if table number is selected
        if not table_number:
            messagebox.showerror("Error", "Please select a table number.")
            return

        # Check if at least one item is selected
        if not any(item["var"].get() == 1 for item in self.selected_items.values()):
            messagebox.showerror("Error", "Please select at least one food item.")
            return

        for item, details in self.selected_items.items():
            if details['var'].get() == 1:
                selected_items_dict[str(index)] = f"{item} ({details['quantity'].get()})"
                index += 1

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"table_number": table_number, "datetime": current_datetime, "selected_items": selected_items_dict}
        self.db.child("orders").push(data)

        #confirmation_message = f"Order for Table {table_number} confirmed.\n\nSelected Items:\n"
        confirmation_message = f"Order for Table {table_number} confirmed.\n\nFood items jo aapne select kiya hai wo hai:\n"
        for item, quantity in selected_items_dict.items():
            confirmation_message += f"{quantity}\n"

        # Speak the confirmation message
        engine.say(confirmation_message)
        engine.runAndWait()

        messagebox.showinfo("Confirmation", confirmation_message)

        # Destroy the current window
        self.destroy()
        

        # Clear selected items for next order
        for item in self.selected_items.values():
            item["var"].set(0)
            item["quantity"].set(1)

        # Add selected table number to the list
        self.selected_table_numbers.append(table_number)


if __name__ == "__main__":
    app = WaiterMenu()
    app.mainloop()
