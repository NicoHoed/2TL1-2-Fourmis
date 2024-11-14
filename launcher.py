import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys



def launch_main(root):
    # Launch the main.py file
    file = os.path.join(os.getcwd(), "main.py")
    root.destroy()
    subprocess.run([sys.executable, file])


def launch_logger(root):
    # Launch the logger.py file
    #script_dir = os.path.dirname(__file__)
    #logger_path = os.path.join(script_dir, "lib", "logger.py")
    #log_dir = os.path.join(script_dir, "log")
    root.destroy()
    subprocess.run([sys.executable, os.path.join(os.getcwd(), 'lib', 'logger.py')])





# Main window
root = tk.Tk()
root.title("Launcher")

# Load the background image
#script_dir = os.path.dirname(__file__)
image_path = os.path.join("img", "ants", "github_Img.jpg")  # Chemin de l'image de fond
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Creation of a canvas for the background image
canvas = tk.Canvas(root, width=background_photo.width(), height=background_photo.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Button for main.py
button_main = tk.Button(root, text="Start colony simulation", command=lambda a=root:launch_main(a))
button_main.pack(pady=10)

# Button for the logger.py

button_logger = tk.Button(root, text="Previous games", command=lambda a=root:launch_logger(a))
button_logger.pack(pady=10)

# Launch main loop

root.mainloop()
