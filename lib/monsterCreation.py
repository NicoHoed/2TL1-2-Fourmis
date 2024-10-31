from json import dump
from os import path

keys = ['name', 'life', 'min_nest_level', 'spawn_prob']

def create_monster(directory: str, param: list):
    global keys
    # Creation of the monster dictionary
    monster = {}
    for key in range(len(keys)):
        monster[keys[key]] = param[key]



    # Save the monster in a JSON file
    with open(path.join(directory , f"{monster['name']}.json"), "w", encoding='utf-8') as file:
        dump(monster, file, indent=4)

    print(f"The monster {monster['name']} was created successfully !")
    print(monster)




if __name__ == '__main__':
    create_monster('../monster', ['test', 10, 2, 30])

