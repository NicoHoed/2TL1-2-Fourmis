import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys


def launch_main(root):
    file = os.path.join(os.getcwd(), "main.py")
    root.destroy()
    subprocess.run([sys.executable, file])


def launch_logger(root):
    #script_dir = os.path.dirname(__file__)
    #logger_path = os.path.join(script_dir, "lib", "logger.py")
    #log_dir = os.path.join(script_dir, "log")
    file = os.path.join(os.getcwd(), "loggerGUI.py")
    root.destroy()
    subprocess.run([sys.executable, file])





root = tk.Tk()
root.title("Launcher")

#script_dir = os.path.dirname(__file__)
image_path = os.path.join("img", "ants", "antColonyAi.jpg")
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=background_photo.width(), height=background_photo.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

button_font = ("Arial", 14, "bold")

button_main = tk.Button(
    root,
    text="Start Colony Simulation",
    command=lambda a=root: launch_main(a),
    width=20,
    height=2,
    font=button_font
)
button_logger = tk.Button(
    root,
    text="Previous Games",
    command=lambda a=root: launch_logger(a),
    width=20,
    height=2,
    font=button_font
)

x_center = background_photo.width() // 2
button_main.place(x=x_center - 100, y=background_photo.height() - 370)  # Adjusted position for larger size
button_logger.place(x=x_center - 100, y=background_photo.height() - 280)  # Adjusted position for larger size


root.mainloop()
