import os
import tkinter as tk
from tkinter import PhotoImage, scrolledtext, Frame, Label
import sys



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

        self.left_frame = Frame(root, width=40)
        self.left_frame.pack(side='left', fill='both', expand=True)


        self.info_box = Frame(self.left_frame, width=40, height=100)
        self.info_box.pack()


        self.nb_ant_var = tk.StringVar()
        self.nb_ant_frame = Frame(self.info_box)
        self.nb_ant_frame.pack()

        self.nb_ant_text = Label(self.nb_ant_frame, text='Nombre de fourmi :')
        self.nb_ant_text.pack(side='left')

        self.nb_ant_label = Label(self.nb_ant_frame, textvariable=self.nb_ant_var)
        self.nb_ant_label.pack(side='left')


        self.nb_ant_worker_var = tk.StringVar()
        self.nb_ant_worker_frame = Frame(self.info_box)
        self.nb_ant_worker_frame.pack()

        self.nb_ant_worker_text = Label(self.nb_ant_worker_frame, text="Nombre d'ouvrière:")
        self.nb_ant_worker_text.pack(side='left')

        self.nb_ant_worker_label = Label(self.nb_ant_worker_frame, textvariable=self.nb_ant_worker_var)
        self.nb_ant_worker_label.pack(side='left')


        self.nb_ant_soldier_var = tk.StringVar()
        self.nb_ant_soldier_frame = Frame(self.info_box)
        self.nb_ant_soldier_frame.pack()

        self.nb_ant_soldier_text = Label(self.nb_ant_soldier_frame, text="Nombre de soldats:")
        self.nb_ant_soldier_text.pack(side='left')

        self.nb_ant_soldier_label = Label(self.nb_ant_soldier_frame, textvariable=self.nb_ant_soldier_var)
        self.nb_ant_soldier_label.pack(side='left')


        self.nest_food_stock_var = tk.StringVar()
        self.nest_food_stock_frame = Frame(self.info_box)
        self.nest_food_stock_frame.pack()

        self.nest_food_stock_text = Label(self.nest_food_stock_frame, text='Quantité de nourriture :')
        self.nest_food_stock_text.pack(side='left')

        self.nest_food_stock_label = Label(self.nest_food_stock_frame, textvariable=self.nest_food_stock_var)
        self.nest_food_stock_label.pack(side='left')


        self.nest_level_var = tk.StringVar()
        self.nest_level_frame = Frame(self.info_box)
        self.nest_level_frame.pack()

        self.nest_level_text = Label(self.nest_level_frame, text='Niveau du nid :')
        self.nest_level_text.pack(side='left')

        self.nest_level_label = Label(self.nest_level_frame, textvariable=self.nest_level_var)
        self.nest_level_label.pack(side='left')


        # ScrolledText widget to display the simulation log
        self.log_display = scrolledtext.ScrolledText(self.left_frame, width=40, height=20)
        self.log_display.pack(fill='both', expand=True)

        # Redirect standard output to the ScrolledText widget
        sys.stdout = TextRedirector(self.log_display)
        
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


    def update_value(self, info: tuple):
        len_ant, ant_capacity, nest_food_stock, nest_food_capacity, nest_level, nb_worker, nb_soldier = info
        self.nb_ant_var.set(f'{len_ant}/{ant_capacity}')
        self.nest_food_stock_var.set(f'{nest_food_stock}/{nest_food_capacity}')
        self.nest_level_var.set(nest_level)
        self.nb_ant_worker_var.set(nb_worker)
        self.nb_ant_soldier_var.set(nb_soldier)


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
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
