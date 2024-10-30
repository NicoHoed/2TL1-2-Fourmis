import os
from random import randint
from time import sleep

from lib.monster import Monster

QUANTITY_FOOD_FOR_LAYING_EGG = 50
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 20
NEST_START_FOOD_STOCK = 50
NEST_START_CAPACITY = 15




class Colony:
    """
    a class for representing a Colony
    """
    def __init__(self, ct_ant = 1, food_stock = NEST_START_FOOD_STOCK, nest_capacity = NEST_START_CAPACITY):
        self.__ctAnt = ct_ant
        self.__ant = []
        self.__nest = Nest(nest_capacity, food_stock)
        self.__queen = Queen(self)

        self.__live = True


        for x in range(self.__ctAnt - 1):
            self.ant.append(Worker(self))

    def manage_ressources(self):
        for ant in self.__ant:
            self.__nest.food_stock -= 1 if ant.role == 'worker' else 3 # for worker or soldier
        self.__nest.food_stock -= 5 #for queen
        if self.__nest.food_stock < 0:
            self.destruct_nest()

    def manage_expansion_nest(self):
        if self.__ctAnt > self.__nest.ant_capacity - 10 and randint(0, 100) <= 10:
            self.__nest.upgrade()

    def react_to_menace(self):
        pass

    def destruct_nest(self):
        print('YOU LOSE')
        self.__live = False


    @property
    def live(self):
        return self.__live


    @property
    def ant(self):
        return self.__ant

    @ant.setter
    def ant(self, new_ant):
        if self.__nest.ant_capacity > self.__ctAnt:
            self.__ant.append(new_ant)
            self.__ctAnt = len(self.__ant)
        else:
            print('no place for the new ant')

    @property
    def ctAnt(self):
        return self.__ctAnt

    @property
    def queen(self):
        return self.__queen

    @property
    def nest(self):
        return self.__nest

    def __iter__(self):
        return iter(self.ant)

    def __str__(self):
        return f'nb ant: {self.ctAnt}, food: {self.nest.food_stock}, nest level: {self.nest.level}'


class Ant:
    """
    a class for representing an Ant
    """
    life_by_role = {'worker': 250, 'soldier': 500, 'queen': 10000}
    def __init__(self, role):
        self.position = [0, 0]
        self.role = role
        self.life = 0
        self.life_span = self.life_by_role[role]


    def do(self):
        self.die()

    def detect_pheromone(self):
        pass


    def die(self):
        self.life += 1
        #print(self.life, self.life_span)
        if self.life == self.life_span:
            print('die')
            return True
        if self.life_span/2 < self.life == randint(0, self.life_span):
            print('die')
            return True

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, x_pos):
        self.position[0] = x_pos

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, y_pos):
        self.position[1] = y_pos

    def __str__(self):
        return self.role


class Queen(Ant):
    """
    a class for representing the unique queen
    """
    def __init__(self, colony):
        super().__init__('queen')
        self.colony = colony

    def lay_eggs(self):
        if randint(0, 100) > 50:
            if self.colony.nest.food_stock > QUANTITY_FOOD_FOR_LAYING_EGG and self.colony.ctAnt > QUANTITY_ANT_FOR_LAYING_SOLDIER:
                self.colony.ant = Worker(self.colony) if randint(0, 100) > 50 else Soldier(self.colony)
            else:
                self.colony.ant = Worker(self.colony)


class Worker(Ant):
    """
    class for representing an ant of type worker
    """
    def __init__(self, colony):
        super().__init__('worker')
        self.colony = colony
        self.have_food = False

    def find_food(self):
        find_food = randint(0, 100) > 10
        self.have_food = find_food
        print('worker find food')
        return find_food

    def drop_food(self):
        self.have_food = False


class Soldier(Ant):
    """
    class for representing an ant of type soldier
    """
    def __init__(self, colony):
        super().__init__('soldier')
        self.colony = colony

    def defend_nest(self):
        pass


class Pheromone:
    """
    a class for representing a pheromone
    """
    def __init__(self, p_type, intensity):
        self.p_type = p_type
        self.intensity = intensity

    def dispel(self):
        self.intensity =- 1


class Nest:
    """
    a class for representing a __nest
    """
    def __init__(self, ant_capacity, food_stock):
        self.ant_capacity = ant_capacity
        self.food_capacity = NEST_START_FOOD_STOCK
        self.food_stock = food_stock
        self.level = 1

    def stock_food(self):
        if self.food_capacity > self.food_stock:
            print('store food')
            self.food_stock += 2
        else:
            print('not enough place to store food')

    def upgrade(self):
        self.ant_capacity += NEST_EXPANSION_RATE
        self.food_capacity += NEST_EXPANSION_RATE
        self.level += 1


def run():
    monstre = []
    for x in os.listdir('monster'):
        monstre.append(Monster(x))

    [print(x) for x in monstre]
    colony = Colony()
    while colony.live:
        colony.queen.lay_eggs()
        for ant in colony:
            if ant.role == 'worker':
                if ant.find_food():
                    colony.nest.stock_food()
                    ant.drop_food()
            colony.ant.remove(ant) if ant.die() else None
        colony.manage_ressources()
        colony.manage_expansion_nest()
        print(colony)

        sleep(1)


if __name__ == '__main__':
    run()

