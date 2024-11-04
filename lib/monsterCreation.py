from json import dump, load
from os import path, listdir

keys = ['name', 'life', 'min_nest_level', 'spawn_prob', 'power']
"""
    name: name of the monster
    life: number of life point -> soldier deal 3 damage, worker deal 1
    min_nest_level: minimum level of the nest for the menace appear
    spaw_prob: 0...100 probability of the menace to spawn, max 1 all 10 cycle
    power: 0...100 probability to kill an ant when fight probability are divided by 3 when fight soldier
"""


def create_monster(directory: str) -> None:
    global keys
    # Creation of the monster dictionary
    monster = {}
    for key in range(len(keys)):
        monster[keys[key]] = input(f"{keys[key]} :")

    # Save the monster in a JSON file
    with open(path.join(directory, f"{monster['name']}.json"), "w", encoding='utf-8') as file:
        dump(monster, file, indent=4)

    print(f"The monster {monster['name']} was created successfully !")
    #print(monster)


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
            new_value = input(f'the monster {monster_data['name']} as the "{key}" fields is empty, new value: ')
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

        print(f"The monster JSON at {file_path} was updated successfully!")
        #print(monster_data)
    else:
        print(f"The monster JSON at {file_path} is already good")


if __name__ == '__main__':

    #create_monster('../monster')

    for predator in listdir('../monster'):
        print('working on', predator)
        update_monster_json(path.join('..', 'monster'), predator)
