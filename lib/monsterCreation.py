from json import dump, load
from os import path

keys = ['name', 'life', 'min_nest_level', 'spawn_prob', 'test']


def create_monster(directory: str, param: list):
    global keys
    # Creation of the monster dictionary
    monster = {}
    for key in range(len(keys)):
        monster[keys[key]] = param[key]

    # Save the monster in a JSON file
    with open(path.join(directory, f"{monster['name']}.json"), "w", encoding='utf-8') as file:
        dump(monster, file, indent=4)

    print(f"The monster {monster['name']} was created successfully !")
    print(monster)


def update_monster_json(directory: str, monster_name: str):
    global keys
    file_path = path.join(directory, f"{monster_name}.json")

    if not path.exists(file_path):
        print(f"The File {file_path} does not exist.")
        return

    # Charging the existing JSON file
    with open(file_path, "r", encoding='utf-8') as file:
        monster_data = load(file)

    # Adding the missing fields with the default values
    for key in keys:
        if key not in monster_data:
            new_value = input(f'the "{key}" fields is empty, new value: ')
            try:
                new_value = int(new_value)

            except:
                pass
            if not isinstance(new_value, int):
                try:
                    new_value = float(new_value)
                except:
                    pass
            print(type(new_value))
            monster_data[key] = new_value

    # Saving the updated file
    with open(file_path, "w", encoding='utf-8') as file:
        dump(monster_data, file, indent=4)

    print(f"The monster JSON at {file_path} was updated successfully!")
    print(monster_data)


if __name__ == '__main__':
    # Creation of a new monster
    #create_monster('../monster', ['test', 10, 2, 30])


    # Json update with the missing fields
    #update_monster_json('../monster', 'test')
    pass
