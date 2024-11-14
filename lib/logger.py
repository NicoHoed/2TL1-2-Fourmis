import os
from datetime import datetime
import csv
from os import path
import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import matplotlib.pyplot as plt



class Logger:
    """
    class use to manage log in a .log file and a sqlite database
    this class support the exportation of sqlite data in a .csv file

    """
    def __init__(self, log_directory: str, export_directory: str, database: str, debugging = False) -> None:
        """init the logger with all info needed
        PRE: None
        POST: None

        """
        self.log_directory = log_directory
        self.export_directory = export_directory
        self.database = database
        self.debugging = debugging
        self.current_table = None

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time
        self.formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

        self.filename = str(self.formatted_datetime) + '.log'
        #self.filename = 'test'

        self.conn = sq.connect(self.database)
        self.cur = self.conn.cursor()
        if not debugging:
            file = open(path.join(self.log_directory, self.filename), 'x')
            file.write('Start of log\n')
            file.close()
            self.create_table()


    def log(self, msg: str) -> None:
        """
        method to log a msg into the current .log file
        PRE: msg end with \n
        POST: None
        """
        with open(path.join(self.log_directory, self.filename), 'a') as file:
            file.write(msg)



    def create_table(self) -> None:
        """
                method to create a table in the sqlite database for logging
                PRE: the database connection must be open
                POST: current_table is set
                """
        self.cur.execute(f"""CREATE TABLE {'table_'}{str(self.formatted_datetime)} (
                                qt_ant INT NOT NULL,
                                max_ant INT NOT NULL,
                                qt_food INT NOT NULL,
                                max_food INT NOT NULL,
                                nest_level INT NOT NULL,
                                qt_worker INT NOT NULL,
                                qt_soldier INT NOT NULL);
                                """)

        self.conn.commit()
        self.current_table = f"{'table_'}{str(self.formatted_datetime)}"


    def get_table(self) -> list[str]:
        """method to get all table in sqlite database
        PRE: the database connexion must be open
        POST: list of all table in the database
        """
        table = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in table.fetchall()]


    def log_db(self, info: tuple[str]) -> None:
        """method to log a tuple of 7 element in the current_table
        PRE: current_table must be set
        POST: None
        """
        self.cur.execute(f"""INSERT INTO {self.current_table} VALUES (
                                ?, ?, ? ,? ,?, ?,?)""", info)

        self.conn.commit()

    def delete_table(self, table: str) -> None:
        """method to delete a table form the current database connexion
        PRE: the database connexion must be open
        POST: None
        """
        self.cur.execute(f"""DROP TABLE IF EXISTS {table}""")

        self.conn.commit()

    def export_data(self, table: str) -> None:
        """method to export data from a table in .csv file
        PRE: the database connexion must be open
        POST: None
        """
        """script based on a script found on gitHub : https://gist.github.com/shitalmule04/82d2091e2f43cb63029500b56ab7a8cc"""

        cur = self.conn.cursor()
        cur.execute(f"""SELECT * from {table}""")
        with open(f"{self.export_directory}/{table[6:]}.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)

        messagebox.showinfo('Success', f'file have been save to {os.path.join(os.getcwd(), self.export_directory, table[6:])}.csv')

    def get_data(self, table: str) -> list[tuple[str]]:
        """method to get all the data of a table from current open connexion
        PRE: the database connexion must be open
        POST: the data of the table
        """
        return self.cur.execute(f"""select * from {table}""").fetchall()



class AppLogger:
    def __init__(self, root: tk.Tk, logger: Logger) -> None:
        self.root = root
        self.logger = logger

        self.root.title('Manage log')
        self.root.geometry('400x150')

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

        self.option = to_human_format(self.logger.get_table())
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
        self.option = to_human_format(self.logger.get_table())
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
        if not self.logger.debugging:
            file_path = os.path.join(os.getcwd(), 'log', f'{table[6:]}.log')
        else:
            file_path = os.path.join(os.getcwd(), '..', 'log', f'{table[6:]}.log')
        #print(file_path)
        threading.Thread(target=lambda: os.system(f'notepad.exe {file_path}')).start()

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


if __name__ == '__main__':
    root = tk.Tk()
    logging = Logger('../log', '../export', '../log/log.db', debugging=True)
    app = AppLogger(root, logging)

    root.mainloop()
