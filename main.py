import os
from random import randint
from time import sleep
import tkinter as tk
import sys


from lib import threat, gui, logger
from config import *

def resource_path(relative_path: str) -> str:
    """ Get the absolute path to a resource within the PyInstaller bundle. """
    # Check if we're running in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts bundled files to sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # Otherwise, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ant:
    """
    a class for representing an Ant
    """

    def __init__(self, role):
        """
        Constructor for initializing an ant instance
        PRE: role is either worker, soldier or queen
        POST: The ant has a lifespan according to its role: life_by_role = {'worker': 250, 'soldier': 500, 'queen': 10000} and a position initialized at [0,0]
        """
        self.position = [0, 0]
        self.role = role
        self.life = 0
        self.life_span = LIFE_BY_ROLE[role]


    def detect_pheromone(self):
        pass

    def track_pheromone(self):
        pass

    def move(self):
        pass


    def die(self):
        """
        Checks if the ant should die
        PRE: The ant should have a valid lifespan
        POST: returns true if the ant has reached or exceeded his lifespan and if the ants life is beyond half its lifespan and a random condition is met.
        """
        self.life += 1
        # print(self.life, self.life_span)
        if self.life == self.life_span:
            #print('die')
            return True
        if self.life_span / 2 < self.life == randint(0, self.life_span):
            #print('die')
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
        if randint(0, 100) > PROBABILITY_TO_LAY_EGG and self.colony.nest.food_stock > QUANTITY_FOOD_FOR_LAYING_EGG:
            #print('lay egg', len([ant for ant in self.colony.ant if ant.role == 'soldier']) < len([ant for ant in self.colony.ant if ant.role == 'worker']) * MAX_SOLDIER_FOR_WORKER / 100)
            if algo_laying_egg(self.colony):
                for x in range(int(self.colony.nest.level/2 if self.colony.nest.level > 1 else 1)):
                    #print('lay egg')
                    self.colony.ant = Worker(self.colony) if randint(0, 100) > 35 else Soldier(self.colony)
            else:
                for x in range(int(self.colony.nest.level/2  if self.colony.nest.level > 1 else 1)):
                    #print('lay egg')
                    self.colony.ant = Worker(self.colony)


class Worker(Ant):
    """
    class for representing an ant of type worker
    """

    def __init__(self, colony):
        """
        Constructor for initializing a worker instance
        PRE: Colony is an instance of Colony and is not none
        POST: The worker is initialized with a reference to the colony and have_food is initialized at False
        """
        super().__init__('worker')
        self.colony = colony
        self.have_food = False

    def find_food(self):
        """
        Simulates the worker finding food
        PRE: The worker must be part of the colony (colony is not None).
        POST:Sets have_food to True if food is found and stays False if not
        """
        find_food = randint(0, 100) > PROBABILITY_TO_FIND_FOOD
        self.have_food = find_food
        #print('worker find food')
        return find_food

    def drop_food(self):
        """
        Simulates the worker dropping food
        PRE: The worker must currently have food (have_food = True)
        POST: have_food is set to False if worker does not have food
        """
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
        self.__p_type = p_type
        self.__intensity = intensity

    def dispel(self):
        self.__intensity = - 1


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
            #print('food stock full')
            pass

    def upgrade(self):
        self.ant_capacity += NEST_EXPANSION_RATE
        self.food_capacity += NEST_EXPANSION_RATE*2
        self.level += 1



class Colony:
    """
    a class for representing a Colony
    """

    def __init__(self, ant_count=1, food_stock=NEST_START_FOOD_STOCK, nest_capacity=NEST_START_CAPACITY):

        """Constructor for initializing the Colony instance with a queen.

        PRE:
            - ant_count (int): The initial count of ants, must be an integer >= 1.
            - food_stock (int): Initial food stock, must be an integer >= 0.
            - nest_capacity (int): Initial nest capacity, must be an integer >= 0.

        POST:
            - The colony is initialized with a queen.
            - If ant_count = 1, the colony contains only the queen and no worker ants.
            - If ant_count > 1, the colony contains (ant_count - 1) worker ants in addition to the queen.
            - The food stock and nest capacity are set as specified.
            - The colony is marked as alive.
        """


        self.__ant = []
        self.__nest = Nest(nest_capacity, food_stock)
        self.__queen = Queen(self)

        self.__live = True

        for x in range(ant_count - 1):
            self.ant.append(Worker(self))

    def manage_ressources(self) -> None:

        """Manages resources by decrementing the food stock based on the consumption of the ants.

        PRE:
            - Food stock in the nest must be defined and non-negative.
            - The colony must have at least one queen ant.

        POST:
            - The food stock is reduced by:
                - 1 unit per worker ant.
                - 3 units per soldier ant.
                - 5 units for the queen.
            - If the food stock becomes negative, the nest is destroyed.
        """


        for ant in self.__ant:
            self.__nest.food_stock -= QT_FOOD_EAT_BY_ROLE[ant.role]
        if self.__nest.food_stock < 0:
            self.destruct_nest()

    def manage_expansion_nest(self) -> None:

        """Expands the nest if the ant population approaches the maximum capacity.

        PRE:
            - The colony must have a valid nest with defined capacity.
            - The colony must have at least one ant.

        POST:
            - If the number of ants exceeds nest capacity - 10 and a random condition is met
              (probability = 10%), the nest's capacity is increased by NEST_EXPANSION_RATE (config).
            - If the conditions are not met, the nest capacity remains unchanged.
        """

        if len(self.__ant) > self.__nest.ant_capacity - 10 and randint(0, 100) <= PROBABILITY_TO_EXPAND_NEST_WHEN_NEST_ALMOST_FULL:
            self.__nest.upgrade()

    def react_to_threat(self, threat: threat.Threat) -> str:

        """Reacts to an external threat by using ants to defend the nest.

        PRE:
            - threat (Threat): A valid object representing the threat, must have:
                - name (str): Name of the threat.
                - life (int): Positive integer representing the threat's health points.
                - power (int): Non-negative integer representing the threat's attack strength.

        POST:
            - Soldier ants attack the threat first, reducing its life points.
            - Worker ants attack if the threat survives, reducing its life points.
            - Soldiers and workers are removed from the colony if killed.
            - If the queen is killed, the nest is destroyed.
            - A message summarizing the encounter is returned.
        """

        text = f'a {threat.name} attack the colony\n'

        #print(f'a {menace.name} attack the colony')
        is_alive = True
        menace_life = threat.life
        menace_power = threat.power

        ants_to_remove = []

        for ant in self.__ant:
            if ant.role == 'soldier':
                menace_life -= SOLDIER_DAMAGE
                if randint(0, 100) < menace_power / 3:
                    ants_to_remove.append(ant)
                if menace_life <= 0:
                    is_alive = False
                    break

        self.__ant = [ant for ant in self.__ant if ant not in ants_to_remove]

        #print('the menace kill ', len(ants_to_remove), 'soldier')
        text += f'the menace kill {len(ants_to_remove)} soldier\n'
        ants_to_remove = []

        if is_alive:
            for ant in self.__ant:
                if ant.role == 'worker':
                    menace_life -= WORKER_DAMAGE
                    if randint(0, 100) < menace_power:
                        ants_to_remove.append(ant)
                    if menace_life <= 0:
                        is_alive = False
                        break

        self.__ant = [ant for ant in self.__ant if ant not in ants_to_remove]

        #print('the menace kill ', len(ants_to_remove), 'worker')
        text += f'the menace kill {len(ants_to_remove)} worker\n'

        if is_alive or len(self.__ant) == 0:
            self.destruct_nest()

        return text



    def destruct_nest(self) -> None:
        """Marks the colony's nest as inactive, representing the destruction of the colony.

        PRE:
            - The nest must exist and currently be active (self.__live = True).

        POST:
            - The nest is marked as inactive by setting self.__live to False.
            - If the nest is already inactive, no changes are made.
            - The colony is effectively considered destroyed.
        """


        if not self.__live:
            return  # The nest is already inactive
        self.__live = False

    @property
    def live(self) -> int:
        return self.__live

    @property
    def ant(self) -> list:
        return self.__ant

    @ant.setter
    def ant(self, new_ant: Ant) -> None:
        if self.__nest.ant_capacity > len(self.ant):
            self.__ant.append(new_ant)
        else:
            #print('no place for the new ant')
            pass


    @property
    def queen(self) -> Queen:
        return self.__queen

    @property
    def nest(self) -> Nest:
        return self.__nest

    def info(self) -> tuple:
        nb_worker = 0
        nb_soldier = 0
        for ant in self.ant:
            if ant.role == 'worker':
                nb_worker += 1
            elif ant.role == 'soldier':
                nb_soldier += 1
        return len(self.__ant), self.nest.ant_capacity, self.nest.food_stock, self.nest.food_capacity, self.nest.level, nb_worker, nb_soldier

    def __iter__(self) -> iter:
        return iter(self.ant)

    def __str__(self) -> str:
        nb_worker = 0
        nb_soldier = 0
        for ant in self.ant:
            if ant.role == 'worker': nb_worker += 1
            elif ant.role == 'soldier': nb_soldier += 1
        return f'nb ant: {len(self.__ant)}, food: {self.nest.food_stock}, nest level: {self.nest.level}, nb worker: {nb_worker}, nb soldier: {nb_soldier}'

    def __repr__(self) -> str:
        nb_worker = 0
        nb_soldier = 0
        for ant in self.ant:
            if ant.role == 'worker':
                nb_worker += 1
            elif ant.role == 'soldier':
                nb_soldier += 1
        return f'nb ant: {len(self.__ant)}, food: {self.nest.food_stock}/{self.nest.food_capacity}, nest level: {self.nest.level}, nb worker: {nb_worker}, nb soldier: {nb_soldier}'



counter = 0

def start(colony: Colony, root: tk.Tk, app: gui.AntSimulationApp, predators: list[threat.Threat], logging: logger.Logger) -> None:
    global counter

    if colony.live:
        counter += 1
        colony.queen.lay_eggs()
        for ant in colony:
            if ant.role == 'worker':
                if ant.find_food():
                    colony.nest.stock_food()
                    ant.drop_food()
            colony.ant.remove(ant) if ant.die() else None
        colony.manage_ressources()
        colony.manage_expansion_nest()

        if counter % 10 == 1:
            for predator in predators:
                if colony.nest.level >= predator.min_nest_level and randint(0, 100) > predator.spawn_prob:
                    text = colony.react_to_threat(predator)
                    logging.log(text)
                    app.console.write(text)
                    break


        app.update_value(colony.info())
        app.update_display()

        logging.log(f'#{counter} - {repr(colony)}\n')
        logging.log_db(colony.info())

        #root.after(100, lambda a=colony, b=root, c=app, d=predators, e=logging: start(a, b, c, d, e))
        root.after(100, start, colony, root, app, predators, logging)

    else:
        app.update_value((0, colony.nest.ant_capacity, colony.nest.food_stock,colony.nest.food_capacity, colony.nest.level, 0, 0))
        app.console.write('colony has been killed')

def run() -> None:

    predators = []
    for x in os.listdir('threats'):
        predators.append(threat.Threat(x)) if x.endswith('.json') else None

    [print(x) for x in predators]
    colony = Colony()

    logging = logger.Logger('log',  'export', os.path.join('log', 'log.db'))



    root = tk.Tk()
    root.geometry('1196x562')
    app = gui.AntSimulationApp(colony, root, os.path.join(resource_path('img'), 'nest')) # initialize GUI

    start(colony, root, app, predators, logging)

    root.mainloop()

    logging.conn.close()
    print('database connection close')


if __name__ == '__main__':
    run()

