import tkinter as tk
from tkinter import PhotoImage

class AntSimulationApp:
    def __init__(self, colony):
        self.colony = colony

        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Ant Simulation")

        # Load images for different colony levels
        self.images = {
            1: PhotoImage(file='../img/nestLVL1.png'),
            2: PhotoImage(file='../img/nestLVL2.png'),
            3: PhotoImage(file='../img/nestLVL3.png'),
            4: PhotoImage(file='../img/nestLVL4.png'),
        }

        # Label to display the current colony image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Start the simulation
        self.update_display()

    def update_display(self):
        """ Update the displayed image based on the colony level. """
        current_level = self.colony.nest.level
        if current_level in self.images:
            self.image_label.config(image=self.images[current_level])
        else:
            print("Image for level", current_level, "not found.")

    def run_simulation(self):
        """ Run the simulation loop. """
        while self.colony.live:
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
            self.root.update()  # Update the Tkinter window

        # Close the window when the simulation ends
        self.root.quit()

    def start(self):
        """ Start the GUI main loop. """
        self.root.mainloop()
