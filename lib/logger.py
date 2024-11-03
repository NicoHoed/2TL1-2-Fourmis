from datetime import datetime
from os import path



class Logger:
    def __init__(self, directory):
        self.directory = directory
        self.ready = True

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        self.filename = str(formatted_datetime) + '.log'
        #self.filename = 'test'

        try:
            file = open(path.join(self.directory, self.filename), 'x')
        except Exception as e:
            print('error with logger', e)
            self.ready = False

    def log(self, msg):
        with open(path.join(self.directory, self.filename), 'a') as file:
            file.write(msg+'\n')
