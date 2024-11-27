import os
import shutil
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


def create_dir(directory):
    if not directory in os.listdir():
        os.mkdir(directory)

def main():
    create_dir('export')
    create_dir('log')
    create_dir('threats')

    # PyInstaller sets the _MEIPASS variable to the temporary directory
    temp_dir = getattr(sys, "_MEIPASS", None)

    if not temp_dir:
        print("Error: Installer is not running from a PyInstaller bundle.")
        sys.exit(1)

    # Destination folder (current working directory)
    dest_dir = os.getcwd()

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


if __name__ == '__main__':
    main()