import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import subprocess


from lib.logger import *

class AppLogger:
    def __init__(self, root: tk.Tk, logger: Logger) -> None:
        self.root = root
        self.logger = logger

        self.root.title('Manage log')
        self.root.geometry('400x150')
        self.root.resizable(width=False, height=False)

        self.root.grid_columnconfigure(1, weight=1)

        self.no_log_text = '------- no log -------'


        self.del_button = ttk.Button(self.root, command=self.del_table, text='delete log')
        self.del_button.grid(row = 1, column = 1, sticky='w')

        self.export_button = ttk.Button(self.root, command=self.export_table, text='export data')
        self.export_button.grid(row=2, column=1, sticky='w')

        self.graphe_button = ttk.Button(self.root, command=self.show_graphe, text='show graphe')
        self.graphe_button.grid(row=3, column=1, sticky='w')

        self.view_log_button = ttk.Button(self.root, command=self.open_log, text='view log')
        self.view_log_button.grid(row=4, column=1, sticky='w')


        self.label_menu = tk.Label(self.root, text='List of log: ')
        self.label_menu.grid(row = 0, column = 0, sticky = 'w')

        self.option = to_human_format(self.logger.get_tables())
        self.menu_choice = tk.StringVar()
        self.menu_choice.set(list(self.option.keys())[0] if self.option else self.disable_button())

        self.menu = ttk.OptionMenu(self.root, self.menu_choice, self.menu_choice.get(),  *self.option)
        self.menu.grid(row = 1, column = 0)




    def del_table(self) -> None:
        table = self.option[self.menu_choice.get()]
        self.logger.delete_table(table)
        if f'{table[6:]}.log' in os.listdir(os.path.join(os.getcwd(), self.logger.log_directory)):
            file_path = os.path.join(os.getcwd(), self.logger.log_directory, f'{table[6:]}.log')
            os.remove(file_path)
        self.option = to_human_format(self.logger.get_tables())
        self.update_option_menu()


    def export_table(self) -> None:
        table = self.option[self.menu_choice.get()]
        #tk.messagebox.showinfo('WIP', 'Not available')
        self.logger.export_data(table)


    def show_graphe(self) -> None:
        """
        table = self.option[self.menu_choice.get()]
        [print(data) for data in self.logger.get_data(table)]
        """
        table = self.option[self.menu_choice.get()]
        data = [record for record in self.logger.get_data(table)]

        # Extract columns from tuples
        nb_ants = [record[0] for record in data]
        food = [record[2] for record in data]
        nb_worker = [record[5] for record in data]
        nb_soldier = [record[6] for record in data]

        # Creation of the x-axis
        time = list(range(1, len(data) + 1))

        # Creation of the graph
        plt.figure(figsize=(10, 6))

        # Line graph for each different categories
        plt.plot(time, nb_ants, label='nb ants', color='blue')
        plt.plot(time, food, label='food', color='green')
        plt.plot(time, nb_worker, label='nb worker', color='red')
        plt.plot(time, nb_soldier, label='nb soldier', color='purple')

        # Add labels and a legend
        plt.xlabel("TimeLine")
        plt.ylabel("Quantity")
        plt.title("Evolution of the Colony")
        plt.legend()
        plt.grid(True)

        # Display graph
        plt.show()

    def open_log(self) -> None:
        table = self.option[self.menu_choice.get()]
        #print(self.menu_choice.get())
        file_path = os.path.join(os.getcwd(), 'log', f'{table[6:]}.log')
        #print(file_path)
        threading.Thread(target=lambda: subprocess.Popen(
            ['notepad.exe', file_path],
            creationflags=subprocess.CREATE_NO_WINDOW  # Suppress console window
        )).start()

    def update_option_menu(self) -> None:
        menu = self.menu["menu"]
        menu.delete(0, "end")
        for string in self.option:
            menu.add_command(label=string,
                             command=lambda value=string: self.menu_choice.set(value))
        #print(self.option)
        self.menu_choice.set(list(self.option.keys())[0] if self.option else self.disable_button())

    def disable_button(self) -> str:
        print('button disable')
        self.del_button['state'] = tk.DISABLED
        self.export_button['state'] = tk.DISABLED
        self.view_log_button['state'] = tk.DISABLED
        self.graphe_button['state'] = tk.DISABLED
        return self.no_log_text


def to_human_format(tables: list[str]) -> dict[str, str]:
    table_dict = {}
    for table in tables:
        timestamp = datetime.strptime(table[6:], "%Y%m%d%H%M%S")
        table_dict[timestamp.strftime("%B %d, %Y, %I:%M:%S %p")] = table

    return table_dict

def run():
    root = tk.Tk()
    logging = Logger('log', 'export', 'log/log.db', create_file=False)
    app = AppLogger(root, logging)

    root.mainloop()


if __name__ == '__main__':
    run()