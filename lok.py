import tkinter as tk
from PIL import ImageTk
import subprocess


bg_colour = "#8B4513"

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def start_second_file():
    # Call the second file using subprocess

    subprocess.run(["python", "/home/harsh/shaswat/wgt.py", "--root", str(root)])
    # Schedule the destruction of the current Tkinter window after a short delay
    root.after(1, root.destroy)

def load_frame1():0
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    logo_img = ImageTk.PhotoImage(file="/home/harsh/shaswat/assets/logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()
    tk.Label(frame1, text="Welcome to our restaurant", bg=bg_colour, fg="white", font=("Shanti", 14)).pack()
    # Increase button font size and width
    tk.Button(frame1, text="Start", font=("Ubuntu", 30), width=20, bg="#28393a", fg="white", cursor="hand2", 
              activebackground="#badee2", activeforeground="black", command=start_second_file).pack(pady=20)

root = tk.Tk()
root.title("Dataintelliage")

# Set fullscreen
root.attributes('-fullscreen', True)

frame1 = tk.Frame(root, bg=bg_colour)
frame2 = tk.Frame(root, bg=bg_colour)

for frame in (frame1, frame2):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

load_frame1()
root.mainloop()
