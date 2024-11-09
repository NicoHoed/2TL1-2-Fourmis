import os
from datetime import datetime
import csv
from os import path
import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox, ttk
import threading



class Logger:
    def __init__(self, log_directory, export_directory, database, debugging = False):
        self.log_directory = log_directory
        self.export_directory = export_directory
        self.database = database
        self.debugging = debugging
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
                file = open(path.join(self.log_directory, self.filename), 'x')
                file.write('Start of log\n')
                file.close()
                self.create_table()
        except Exception as e:
            print('error with logger: ', e)
            self.is_ready = False





    def log(self, msg):
        with open(path.join(self.log_directory, self.filename), 'a') as file:
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

    def export_data(self, table):
        """script find on gitHub : https://gist.github.com/shitalmule04/82d2091e2f43cb63029500b56ab7a8cc and modify"""
        cur = self.conn.cursor()
        cur.execute(f"""SELECT * from {table}""")
        with open(f"{self.export_directory}/{table[6:]}.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)

        messagebox.showinfo('Success', f'file have been save to {os.path.join(os.getcwd(), self.export_directory, table[6:])}.csv')



class AppLogger:
    def __init__(self, root: tk.Tk, logger: Logger):
        self.root = root
        self.logger = logger

        self.root.title('Manage log')
        self.root.geometry('250x250')

        self.root.grid_columnconfigure(1, weight=1)

        self.no_log_text = '------- no log -------'


        self.del_button = ttk.Button(self.root, command=self.del_table, text='delete log')
        self.del_button.grid(row = 0, column = 1, sticky='w')

        self.export_button = ttk.Button(self.root, command=self.export_table, text='export data')
        self.export_button.grid(row=1, column=1, sticky='w')

        self.graphe_button = ttk.Button(self.root, command=self.show_graphe, text='show graphe')
        self.graphe_button.grid(row=2, column=1, sticky='w')

        self.view_log_button = ttk.Button(self.root, command=self.open_log, text='view log')
        self.view_log_button.grid(row=3, column=1, sticky='w')


        self.option = logger.get_table()
        self.menu_choice = tk.StringVar()
        self.menu_choice.set(self.option[0] if self.option else self.disable_button())

        self.menu = ttk.OptionMenu(self.root, self.menu_choice, self.menu_choice.get(),  *self.option)
        self.menu.grid(row = 0, column = 0)




    def del_table(self):
        self.logger.delete_table(self.menu_choice.get())
        if f'{self.menu_choice.get()[6:]}.log' in os.listdir(os.path.join(os.getcwd(), self.logger.log_directory)):
            file_path = os.path.join(os.getcwd(), self.logger.log_directory, f'{self.menu_choice.get()[6:]}.log')
            os.remove(file_path)
        self.option = self.logger.get_table()
        self.update_option_menu()


    def export_table(self):
        #tk.messagebox.showinfo('WIP', 'Not available')
        self.logger.export_data(self.menu_choice.get())


    def show_graphe(self):
        print(self.menu_choice.get())

    def open_log(self):
        #print(self.menu_choice.get())
        if not self.logger.debugging:
            file_path = os.path.join(os.getcwd(), 'log', f'{self.menu_choice.get()[6:]}.log')
        else:
            file_path = os.path.join(os.getcwd(), '..', 'log', f'{self.menu_choice.get()[6:]}.log')
        #print(file_path)
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
    logging = Logger('../log', '../export', '../log/log.db', debugging=True)
    app = AppLogger(root, logging)

    root.mainloop()
