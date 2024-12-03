import os
from datetime import datetime
import csv
from os import path
import sqlite3 as sq
from tkinter import messagebox


class Logger:
    """
    class use to manage log in a .log file and a sqlite database
    this class support the exportation of sqlite data in a .csv file

    """
    def __init__(self, log_directory: str, export_directory: str, database: str, create_file: bool = True) -> None:
        """init the logger with all info needed
        PRE: a log, export directory, a sqlite db
        POST: the log, except and db are set, the file is create for logging, the db is connected and table is created to log.
        RAISES: sqlite3.Error is throw if db cannot be connected or IOError file cannot be created
        """
        if not os.path.exists(export_directory) or not os.path.exists(log_directory):
            raise FileNotFoundError
        self.log_directory = log_directory
        self.export_directory = export_directory
        self.database = database
        self.create_file = create_file
        self.current_table = None

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time
        self.formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

        self.filename = str(self.formatted_datetime) + '.log'
        #self.filename = 'test'

        self.conn = sq.connect(self.database)
        self.cur = self.conn.cursor()
        if create_file:
            file = open(path.join(self.log_directory, self.filename), 'x')
            file.write('Start of log\n')
            file.close()
            self.create_table()


    def log(self, msg: str) -> None:
        """
        method to log a msg into the current .log file
        PRE: None
        POST: the msg is added int the log file.
        RAISES: IOError is throw if the file cannot be write
        """
        with open(path.join(self.log_directory, self.filename), 'a') as file:
            file.write(msg)



    def create_table(self) -> None:
        """
                method to create a table in the sqlite database for logging
                PRE: the database connection must be open
                POST: a table is created in the db and the current_table var is set for logging msg
                RAISES: sqlite3.Error is throw if the db is not connected
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


    def get_tables(self) -> list[str]:
        """method to get all tables in sqlite database
        PRE: the database connexion must be open
        POST: return list of all tables in the database
        RAISES: sqlite3.Error is throw if the db is not connected
        """
        table = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in table.fetchall()]

    def log_db(self, info: tuple) -> None:
        """method to log a tuple of 7 element in the current_table
        PRE: current_table must != None
        POST: the info is log into the db in a new line
        RAISES: sqlite3.Error is throw if db is not connected or the table does not exist
        """
        self.cur.execute(f"""INSERT INTO {self.current_table} VALUES (
                                ?, ?, ? ,? ,?, ?,?)""", info)

        self.conn.commit()

    def delete_table(self, table: str) -> None:
        """method to delete a table form the current database connexion
        PRE: None
        POST: the table is deleted if exists
        RAISES: sqlite3.Error is throw is sqlite database is not connected
        """
        self.cur.execute(f"""DROP TABLE IF EXISTS {table}""")

        self.conn.commit()

    def export_data(self, table: str) -> None:
        """method to export data from a table in .csv file
        PRE: the database connexion must be open, teh table must exist in the current database
        POST: the table is export in csv in the export folder
        RAISES: IOError if the export file cannot be created or sqlite3.Error if sqlite database is not connected
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
        PRE: the database connexion must be open, the table exist in the database
        POST: return a tuple with the info of the table
        RAISES: sqlite3.Error if the database is not connected
        """
        return self.cur.execute(f"""select * from {table}""").fetchall()



