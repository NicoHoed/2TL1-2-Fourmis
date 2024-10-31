from json import dump, load
from os import path

keys = ['name', 'life', 'min_nest_level', 'spawn_prob']


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


def update_monster_json(directory: str, monster_name: str, default_values: dict):
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
            monster_data[key] = default_values.get(key, None)

    # Saving the updated file
    with open(file_path, "w", encoding='utf-8') as file:
        dump(monster_data, file, indent=4)

    print(f"The monster JSON at {file_path} was updated successfully!")
    print(monster_data)


if __name__ == '__main__':
    # Creation of a new monster
    create_monster('../monster', ['test', 10, 2, 30])

    # Default values for the required fields
    default_values = {
        "name": "unknown",
        "life": 100,
        "min_nest_level": 1,
        "spawn_prob": 10
    }

    # Json update with the missing fields
    update_monster_json('../monster', 'test', default_values)
