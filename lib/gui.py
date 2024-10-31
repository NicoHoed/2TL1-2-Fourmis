import os
import tkinter as tk
from tkinter import PhotoImage

class AntSimulationApp:
    def __init__(self, colony, root, img_nest):
        self.colony = colony

        # Initialize the Tkinter window
        self.root = root
        self.root.title("Ant Simulation")

        # Load images for different colony levels
        # Adjust the path to be relative from the current script location
        self.images = {
            1: PhotoImage(file=os.path.join(img_nest, 'nestLVL1.png')),
            2: PhotoImage(file=os.path.join(img_nest, 'nestLVL2.png')),
            3: PhotoImage(file=os.path.join(img_nest, 'nestLVL3.png')),
            4: PhotoImage(file=os.path.join(img_nest, 'nestLVL4.png')),
        }

        # Label to display the current colony image
        self.image_label = tk.Label(self.root)
        self.image_label.pack(side='right')

        # Start the simulation
        self.update_display()
        #self.run_simulation()  # Start the simulation immediately

    def update_display(self):
        """ Update the displayed image based on the colony level. """
        current_level = self.colony.nest.level
        if current_level in self.images:
            self.image_label.config(image=self.images[current_level])
        elif current_level > len(self.images):
            pass

    #def run_simulation(self):
    #    """ Run the simulation loop. """
    #    if self.colony.live:
    #        self.colony.queen.lay_eggs()
    #        for ant in self.colony:
    #            if ant.role == 'worker':
    #                if ant.find_food():
    #                    self.colony.nest.stock_food()
    #                    ant.drop_food()
    #            self.colony.ant.remove(ant) if ant.die() else None
    #        self.colony.manage_ressources()
    #        self.colony.manage_expansion_nest()
    #        print(self.colony)

    #        # Update the display after each simulation step
    #        self.update_display()

    #        # Schedule the next simulation step
    #        self.root.after(1000, self.run_simulation)  # Update every 1000 ms (1 second)
    #    else:
    #        print("Simulation ended.")
    #        self.root.quit()
