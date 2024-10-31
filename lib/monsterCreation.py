import json


def create_monster(name, life, min_nest_level, spawn_prob):
    # Creation of the monster dictionary
    monster = {
        "name": name,
        "life": life,
        "min_nest_level": min_nest_level,
        "spawn_prob": spawn_prob
    }

    # Convert the dictionary in JSON
    monster_json = json.dumps(monster, ident=4)

    # Save the monster in a JSON file
    with open(f"{name}.json", "w") as file:
        file.write(monster_json)

    print(f"The monster {name} was created successfully !")
    print(monster_json)

