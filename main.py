import os
from random import randint
from time import sleep
import tkinter as tk


from lib import monster, gui


QUANTITY_FOOD_FOR_LAYING_EGG = 10
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 100
NEST_START_FOOD_STOCK = 50
NEST_START_CAPACITY = 15
MAX_SOLDIER_FOR_WORKER = 50 # 0...100 the max soldier per worker in %


class Colony:
    """
    a class for representing a Colony
    """

    def __init__(self, ct_ant=1, food_stock=NEST_START_FOOD_STOCK, nest_capacity=NEST_START_CAPACITY):
        self.__ant = []
        self.__nest = Nest(nest_capacity, food_stock)
        self.__queen = Queen(self)

        self.__live = True

        for x in range(ct_ant - 1):
            self.ant.append(Worker(self))

    def manage_ressources(self):
        for ant in self.__ant:
            self.__nest.food_stock -= 1 if ant.role == 'worker' else 3  # for worker or soldier
        self.__nest.food_stock -= 5  # for queen
        if self.__nest.food_stock < 0:
            self.destruct_nest()

    def manage_expansion_nest(self):
        if len(self.__ant) > self.__nest.ant_capacity - 10 and randint(0, 100) <= 10:
            self.__nest.upgrade()

    def react_to_menace(self, menace) -> None:
        print(f'a {menace.name} attack the colony')
        isAlive = True
        menace_life = menace.life
        menace_power = menace.power

        ants_to_remove = []

        for ant in self.__ant:
            if ant.role == 'soldier':
                menace_life -= 3
                if randint(0, 100) < menace_power / 3:
                    ants_to_remove.append(ant)
                if menace_life <= 0:
                    isAlive = False
                    break

        self.__ant = [ant for ant in self.__ant if ant not in ants_to_remove]

        print('the menace kill ', len(ants_to_remove), 'soldier')
        ants_to_remove = []

        if isAlive:
            for ant in self.__ant:
                if ant.role == 'worker':
                    menace_life -= 1
                    if randint(0, 100) < menace_power:
                        ants_to_remove.append(ant)
                    if menace_life <= 0:
                        isAlive = False
                        break

        self.__ant = [ant for ant in self.__ant if ant not in ants_to_remove]

        print('the menace kill ', len(ants_to_remove), 'worker')

        if isAlive or len(self.__ant) == 0:
            self.destruct_nest()



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
        if self.__nest.ant_capacity > len(self.ant):
            self.__ant.append(new_ant)
        else:
            print('no place for the new ant')


    @property
    def queen(self):
        return self.__queen

    @property
    def nest(self):
        return self.__nest

    def __iter__(self):
        return iter(self.ant)

    def __str__(self):
        nb_worker = 0
        nb_soldier = 0
        for ant in self.ant:
            if ant.role == 'worker': nb_worker += 1
            elif ant.role == 'soldier': nb_soldier += 1
        return f'nb ant: {len(self.__ant)}, food: {self.nest.food_stock}, nest level: {self.nest.level}, nb worker: {nb_worker}, nb soldier: {nb_soldier}'


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
        # print(self.life, self.life_span)
        if self.life == self.life_span:
            print('die')
            return True
        if self.life_span / 2 < self.life == randint(0, self.life_span):
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
        if randint(0, 100) > 25 and self.colony.nest.food_stock > QUANTITY_FOOD_FOR_LAYING_EGG:
            print('lay egg', len([ant for ant in self.colony.ant if ant.role == 'soldier']) < len([ant for ant in self.colony.ant if ant.role == 'worker']) * MAX_SOLDIER_FOR_WORKER / 100)
            if len(self.colony.ant) > QUANTITY_ANT_FOR_LAYING_SOLDIER and len([ant for ant in self.colony.ant if ant.role == 'soldier']) < len([ant for ant in self.colony.ant if ant.role == 'worker']) * MAX_SOLDIER_FOR_WORKER / 100:
                self.colony.ant = Worker(self.colony) if randint(0, 100) > 35 else Soldier(self.colony)
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
        #print('worker find food')
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
        self.intensity = - 1


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
            #print('store food')
            self.food_stock += 4
        else:
            print('food stock full')

    def upgrade(self):
        self.ant_capacity += NEST_EXPANSION_RATE
        self.food_capacity += NEST_EXPANSION_RATE*2
        self.level += 1


def start(colony, root, app, predators):
    if colony.live:
        colony.queen.lay_eggs()
        for ant in colony:
            if ant.role == 'worker':
                if ant.find_food():
                    colony.nest.stock_food()
                    ant.drop_food()
            colony.ant.remove(ant) if ant.die() else None
        colony.manage_ressources()
        colony.manage_expansion_nest()

        for predator in predators:
            if colony.nest.level >= predator.min_nest_level and randint(0, 100) > predator.spawn_prob:
                colony.react_to_menace(predator)
                break

        print(colony)


        app.update_display()

        root.after(100, lambda a=colony, b=root, c=app, d=predators: start(a, b, c, d))

def run():
    predators = []
    for x in os.listdir('monster'):
        predators.append(monster.Monster(x))

    [print(x) for x in predators]
    colony = Colony()

    root = tk.Tk()
    root.geometry('1196x562')
    app = gui.AntSimulationApp(colony, root, 'img/resized')  # Initialize the GUI application with the colony

    start(colony, root, app, predators)

    root.mainloop()




if __name__ == '__main__':
    run()

