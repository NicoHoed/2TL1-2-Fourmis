import os
from datetime import datetime
from os import path
import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox, ttk
import threading



class Logger:
    def __init__(self, directory, database, debugging = False):
        self.directory = directory
        self.database = database
        self.is_ready = True
        self.current_table = None

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time
        self.formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

        self.filename = str(self.formatted_datetime) + '.log'
        #self.filename = 'test'

        try:
            self.conn = sq.connect(self.database)
            self.cur = self.conn.cursor()
            if not debugging:
                file = open(path.join(self.directory, self.filename), 'x')
                file.close()
                self.create_table()
        except Exception as e:
            print('error with logger: ', e)
            self.is_ready = False





    def log(self, msg):
        with open(path.join(self.directory, self.filename), 'a') as file:
            file.write(msg+'\n')

    def get_table(self):
        table = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in table.fetchall()]

    def create_table(self):
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

    def log_db(self, info):
        self.cur.execute(f"""INSERT INTO {self.current_table} VALUES (
                                ?, ?, ? ,? ,?, ?,?)""", info)

        self.conn.commit()

    def delete_table(self, table):
        self.cur.execute(f"""DROP TABLE IF EXISTS {table}""")

        self.conn.commit()



class AppLogger:
    def __init__(self, root: tk.Tk, logger: Logger):
        self.root = root
        self.logger = logger

        self.root.title('Manage log')
        self.root.geometry('250x250')

        self.root.grid_columnconfigure(1, weight=1)

        self.no_log_text = '------- no log -------'


        self.option = logger.get_table()
        self.menu_choice = tk.StringVar()
        self.menu_choice.set(self.option[0] if self.option else self.disable_button())

        self.menu = ttk.OptionMenu(self.root, self.menu_choice, self.menu_choice.get(),  *self.option)
        self.menu.grid(row = 0, column = 0)

        self.del_button = ttk.Button(self.root, command=self.del_table, text='delete log')
        self.del_button.grid(row = 0, column = 1, sticky='w')

        self.export_button = ttk.Button(self.root, command=self.export_table, text='export data')
        self.export_button.grid(row=1, column=1, sticky='w')

        self.graphe_button = ttk.Button(self.root, command=self.show_graphe, text='show graphe')
        self.graphe_button.grid(row=2, column=1, sticky='w')

        self.view_log_button = ttk.Button(self.root, command=self.open_log, text='view log')
        self.view_log_button.grid(row=3, column=1, sticky='w')


    def del_table(self):
        self.logger.delete_table(self.menu_choice.get())
        if f'{self.menu_choice.get()[6:]}.log' in os.listdir(os.path.join(os.getcwd(), self.logger.directory)):
            file_path = os.path.join(os.getcwd(), self.logger.directory, f'{self.menu_choice.get()[6:]}.log')
            os.remove(file_path)
        self.option = self.logger.get_table()
        self.update_option_menu()


    def export_table(self):
        tk.messagebox.showinfo('WIP', 'Not available')

    def show_graphe(self):
        print(self.menu_choice.get())

    def open_log(self):
        print(self.menu_choice.get())
        file_path = os.path.join(os.getcwd(), 'log', f'{self.menu_choice.get()[6:]}.log')
        threading.Thread(target=lambda: os.system(f'notepad.exe {file_path}')).start()

    def update_option_menu(self):
        menu = self.menu["menu"]
        menu.delete(0, "end")
        for string in self.option:
            menu.add_command(label=string,
                             command=lambda value=string: self.menu_choice.set(value))
        self.menu_choice.set(self.option[0] if self.option else self.disable_button())

    def disable_button(self):
        #print('button disable')
        self.del_button['state'] = tk.DISABLED
        self.export_button['state'] = tk.DISABLED
        self.view_log_button['state'] = tk.DISABLED
        self.graphe_button['state'] = tk.DISABLED
        return self.no_log_text


if __name__ == '__main__':
    root = tk.Tk()
    logging = Logger('../log', '../log/log.db', debugging=False)
    app = AppLogger(root, logging)

    root.mainloop()
