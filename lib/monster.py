from json import load
from os import path
import json

class Monster:
    def __init__(self, file: str):
        with open(path.join('monster', file) if __name__ != '__main__' else path.join('..', 'monster', file), 'r', encoding='utf-8') as file:
            try:
                data = dict(load(file))
                self.life = data['life']
                self.name = data['name']
                self.min_nest_level = data['min_nest_level']
                self.spawn_prob = data['spawn_prob']
                self.power = data['power']
            except:
                print('error')

    def __str__(self) -> str:
        return self.name


if __name__ == '__main__':
    spider = Monster('spider.json')

