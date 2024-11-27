import threading
import tkinter as tk
from tkinter import ttk, Toplevel
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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

        self.graphe_button = ttk.Button(self.root, command=self.show_graphe, text='show graph')
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


    def _total_increments(self, data: list[int]) -> int:
        total = 0
        for i in range(1, len(data)):
            if data[i] > data[i-1]:
                total += data[i] - data[i-1]
        return total


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

        table = self.option[self.menu_choice.get()]
        data = [record for record in self.logger.get_data(table)]

        nb_ants = [record[0] for record in data]
        food = [record[2] for record in data]
        nb_worker = [record[5] for record in data]
        nb_soldier = [record[6] for record in data]

        time = list(range(1, len(data) + 1))

        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(time, nb_ants, label='Ants', color='blue')
        ax.plot(time, food, label='Food', color='green')
        ax.plot(time, nb_worker, label='Workers', color='red')
        ax.plot(time, nb_soldier, label='Soldiers', color='purple')

        ax.set_xlabel("Timeline")
        ax.set_ylabel("Quantity")
        ax.set_title("Evolution of the Colony")
        ax.legend()
        ax.grid(True)

        total_ants = self._total_increments(nb_ants)
        total_workers = self._total_increments(nb_worker)
        total_soldiers = self._total_increments(nb_soldier)
        total_food = self._total_increments(food)
        total_time = len(time)

        graph_window = Toplevel()
        graph_window.title("Colony Evolution Graph")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        canvas.draw()

        info_frame = tk.Frame(graph_window)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(info_frame, text="Colony Evolution Summary", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        tk.Label(info_frame, text=f"Total Ants: {total_ants}").pack(anchor="w")
        tk.Label(info_frame, text=f"Total Workers: {total_workers}").pack(anchor="w")
        tk.Label(info_frame, text=f"Total Soldiers: {total_soldiers}").pack(anchor="w")
        tk.Label(info_frame, text=f"Total Food: {total_food}").pack(anchor="w")
        tk.Label(info_frame, text=f"Total Time: {total_time}").pack(anchor="w")

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