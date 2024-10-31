import os
import tkinter as tk
from tkinter import PhotoImage

class AntSimulationApp:
    def __init__(self, colony):
        self.colony = colony

        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Ant Simulation")

        # Load images for different colony levels
        # Adjust the path to be relative from the current script location
        base_path = os.path.dirname(__file__)  # Get the directory of the current file
        self.images = {
            1: PhotoImage(file=os.path.join(base_path, '../img/nestLVL1.png')),
            2: PhotoImage(file=os.path.join(base_path, '../img/nestLVL2.png')),
            3: PhotoImage(file=os.path.join(base_path, '../img/nestLVL3.png')),
            4: PhotoImage(file=os.path.join(base_path, '../img/nestLVL4.png')),
        }

        # Label to display the current colony image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Start the simulation
        self.update_display()
        self.run_simulation()  # Start the simulation immediately

    def update_display(self):
        """ Update the displayed image based on the colony level. """
        current_level = self.colony.nest.level
        if current_level in self.images:
            self.image_label.config(image=self.images[current_level])
        else:
            print("Image for level", current_level, "not found.")

    def run_simulation(self):
        """ Run the simulation loop. """
        if self.colony.live:
            self.colony.queen.lay_eggs()
            for ant in self.colony:
                if ant.role == 'worker':
                    if ant.find_food():
                        self.colony.nest.stock_food()
                        ant.drop_food()
                self.colony.ant.remove(ant) if ant.die() else None
            self.colony.manage_ressources()
            self.colony.manage_expansion_nest()
            print(self.colony)

            # Update the display after each simulation step
            self.update_display()

            # Schedule the next simulation step
            self.root.after(1000, self.run_simulation)  # Update every 1000 ms (1 second)
        else:
            print("Simulation ended.")
            self.root.quit()

    def start(self):
        """ Start the GUI main loop. """
        self.root.mainloop()
