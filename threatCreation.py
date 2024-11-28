from json import load
from os import path
import tkinter as tk
from json import dump
import os
import sys

keys = ['name', 'life', 'min_nest_level', 'spawn_prob', 'power']
"""
    name: name of the threats
    life: number of life point -> soldier deal 3 damage, worker deal 1
    min_nest_level: minimum level of the nest for the menace appear
    spaw_prob: 0...100 probability of the menace to spawn, max 1 all 10 cycle
    power: 0...100 probability to kill an ant when fight probability are divided by 3 when fight soldier
"""


def resource_path(relative_path: str) -> str:
    """ Get the absolute path to a resource within the PyInstaller bundle. """
    # Check if we're running in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts bundled files to sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # Otherwise, use the current directory
        base_path = os.path.abspath("lib")

    return os.path.join(base_path, relative_path)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("threat creation")
        self.root.geometry("250x150")
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap(resource_path('img/icon/logo.ico'))

        self.label_list = []
        self.entry_list = []
        self.var_entry = []
        self.sub_frame_list = []

        for entry in keys:
            frame = tk.Frame(root)
            self.label_list.append(tk.Label(frame, text=f'{entry}: ').pack(side='left'))
            var = tk.StringVar()
            self.entry_list.append(tk.Entry(frame, textvariable=var).pack(side='left'))
            self.var_entry.append(var)
            self.sub_frame_list.append(frame)
            frame.pack()

        self.done_button = tk.Button(root, command=self.done, text='Done')
        self.done_button.pack()


    def done(self):
        value = [x.get() for x in self.var_entry]

        if '' in value:
            print(value)
            return

        dict_value = {}
        for val in range(len(value)):
            dict_value[keys[val]] = value[val]


        with open(resource_path(f'threats/{value[0]}.json'), 'x', encoding='utf-8') as file:
            dump(dict_value, file, indent=4)
            root.quit()







def create_monster(directory: str) -> None:
    global keys
    # Creation of the threats dictionary
    monster = {}
    for key in range(len(keys)):
        monster[keys[key]] = input(f"{keys[key]} :")

    # Save the threats in a JSON file
    with open(path.join(directory, f"{monster['name']}.json"), "w", encoding='utf-8') as file:
        dump(monster, file, indent=4)

    print(f"The threats {monster['name']} was created successfully !")
    #print(threats)


def update_monster_json(directory: str, file: str) -> None:
    global keys
    file_path = path.join(directory, file)

    if not path.exists(file_path):
        print(f"The File {file_path} does not exist.")
        return

    # Charging the existing JSON file
    with open(file_path, "r", encoding='utf-8') as file:
        monster_data = load(file)

    # Adding the missing fields with the default values
    needRewrite = False
    for key in keys:
        if key not in monster_data:
            new_value = input(f'the threats {monster_data['name']} as the "{key}" fields is empty, new value: ')
            try:
                new_value = int(new_value)

            except:
                pass
            if not isinstance(new_value, int):
                try:
                    new_value = float(new_value)
                except:
                    pass
            monster_data[key] = new_value
            needRewrite = True

    # Saving the updated file
    if needRewrite:
        with open(file_path, "w", encoding='utf-8') as file:
            dump(monster_data, file, indent=4)

        print(f"The threats JSON at {file_path} was updated successfully!")
        #print(monster_data)
    else:
        print(f"The threats JSON at {file_path} is already good")


if __name__ == '__main__':

    #create_monster('../threats')

    #for predator in listdir('../threats'):
    #    print('working on', predator)
    #    update_monster_json(path.join('..', 'threats'), predator)
    root = tk.Tk()
    app = App(root)
    root.mainloop()
