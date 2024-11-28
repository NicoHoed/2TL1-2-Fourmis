import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import winshell


class GUI:
    def __init__(self):
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Installer")

        # Variables
        self.install_dir_var = tk.StringVar(value=os.getcwd())
        self.shortcut_var = tk.BooleanVar()

        # UI Elements
        tk.Label(self.root, text="Select Installation Directory:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.install_dir_var, width=50).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.select_install_directory).pack(pady=5)

        tk.Checkbutton(self.root, text="Create Desktop Shortcut", variable=self.shortcut_var).pack(pady=5)

        tk.Button(self.root, text="Install", command=self.install).pack(pady=20)

        self.root.mainloop()

    def select_install_directory(self):
        """Open a dialog to select the installation directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.install_dir_var.set(os.path.join(directory, 'colonyConnect'))

    def install(self):
        create_dir(self.install_dir_var.get())
        create_dir(os.path.join(self.install_dir_var.get(),'export'))
        create_dir(os.path.join(self.install_dir_var.get(),'log'))
        create_dir(os.path.join(self.install_dir_var.get(),'threats'))

        if self.shortcut_var.get():
            self.create_shortcut()

        # PyInstaller sets the _MEIPASS variable to the temporary directory
        temp_dir = getattr(sys, "_MEIPASS", None)

        if not temp_dir:
            print("Error: Installer is not running from a PyInstaller bundle.")
            sys.exit(1)

        # Destination folder (current working directory)
        dest_dir = self.install_dir_var.get()

        # List of files to move
        files_to_move = os.listdir(resource_path('exe'))

        print(f"Installing files to: {dest_dir}\n")

        for filename in files_to_move:
            source_path = os.path.join(temp_dir, "exe", filename)
            dest_path = os.path.join(dest_dir, filename)

            if os.path.exists(source_path):
                print(f"Copying {filename}...")
                shutil.copy(source_path, dest_path)
            else:
                print(f"Error: {filename} not found in temporary directory.")
                sys.exit(1)

        print("Installation completed successfully.")
        self.root.destroy()
        sys.exit()


    def create_shortcut(self):
        # Get the path to the Startup folder

        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


        # Create the shortcut in the startup folder
        shortcut_path = os.path.join(desktop, f"colonyConnect.lnk")
        with winshell.shortcut(str(shortcut_path)) as link:
            link.path = os.path.join(self.install_dir_var.get(), 'launcher.exe')
            link.working_directory = self.install_dir_var.get()
            link.description = f"Shortcut to colonyConnect"

        print(f"Shortcut created at: {shortcut_path}")


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


def create_dir(directory):
    print('create dir in ', os.path.join(directory, '..'))
    if not os.path.split(directory)[1] in os.listdir(os.path.join(directory, '..')):
        os.mkdir(directory)





if __name__ == '__main__':
    a = GUI()