import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys


def resource_path(relative_path: str) -> str:
    """ Get the absolute path to a resource within the PyInstaller bundle. """
    # Check if we're running in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts bundled files to sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # Otherwise, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def launch_main(root):
    file = os.path.join(os.getcwd(), "colonyConnect.exe")
    root.destroy()
    subprocess.run([file])


def launch_logger(root):
    #script_dir = os.path.dirname(__file__)
    #logger_path = os.path.join(script_dir, "lib", "logger.py")
    #log_dir = os.path.join(script_dir, "log")
    file = os.path.join(os.getcwd(), "logger.exe")
    root.destroy()
    subprocess.run([file])





root = tk.Tk()
root.title("Launcher")
root.iconbitmap(resource_path('img/icon/logo.ico'))


#script_dir = os.path.dirname(__file__)
image_path = os.path.join(resource_path("img"), "ants", "antColonyAi.jpg")
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
