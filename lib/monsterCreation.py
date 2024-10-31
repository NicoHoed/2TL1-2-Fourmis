from json import dump
from os import path

def create_monster(dir, name, life, min_nest_level, spawn_prob):
    # Creation of the monster dictionary
    monster = {
        "name": name,
        "life": life,
        "min_nest_level": min_nest_level,
        "spawn_prob": spawn_prob
    }



    # Save the monster in a JSON file
    with open(path.join(dir , f"{name}.json"), "w", encoding='utf-8') as file:
        dump(monster, file, indent=4)

    print(f"The monster {name} was created successfully !")
    print(monster)


if __name__ == '__main__':
    create_monster('../monster', 'test', 10, 2, 30)

