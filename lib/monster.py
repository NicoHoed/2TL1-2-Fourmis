from json import load
from os import path

class Monster:
    def __init__(self, file: str):
        with open(path.join('monster', file) if __name__ != '__main__' else path.join('..', 'monster', file), 'r', encoding='utf-8') as file:
            try:
                data = dict(load(file))
                self.life = data['life']
                self.name = data['name']
            except:
                print('error')

    def __str__(self):
        return self.name


if __name__ == '__main__':
    spider = Monster('spider.json')