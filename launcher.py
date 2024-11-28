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
    file = os.path.join(os.getcwd(), "logger.exe")
    root.destroy()
    subprocess.run([file])


root = tk.Tk()
root.title("Launcher")
root.iconbitmap(resource_path('img/icon/logo.ico'))

# Charger et redimensionner l'image de fond
image_path = os.path.join(resource_path("img"), "ants", "antColonyAi.jpg")
background_image = Image.open(image_path)

# Redimensionner l'image à 800x700 pixels
new_width = 800
new_height = 700
background_image = background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Convertir l'image redimensionnée en un objet PhotoImage
background_photo = ImageTk.PhotoImage(background_image)

# Configurer le canevas à la nouvelle taille
canvas = tk.Canvas(root, width=new_width, height=new_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Définir la police des boutons
button_font = ("Arial", 14, "bold")

# Bouton pour lancer la simulation principale
button_main = tk.Button(
    root,
    text="Start Colony Simulation",
    command=lambda a=root: launch_main(a),
    width=20,
    height=2,
    font=button_font
)

# Bouton pour ouvrir les anciens jeux
button_logger = tk.Button(
    root,
    text="Previous Games",
    command=lambda a=root: launch_logger(a),
    width=20,
    height=2,
    font=button_font
)

# Placer les boutons au centre, ajustés pour la nouvelle taille de l'image
x_center = new_width // 2
button_main.place(x=x_center - 100, y=new_height - 200)  # Position ajustée
button_logger.place(x=x_center - 100, y=new_height - 120)  # Position ajustée

root.mainloop()
