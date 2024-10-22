from random import randint
from time import sleep

COST_OF_ANT = 0.5
QUANTITY_FOOD_FOR_LAYING_EGG = 50
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 20
NEST_START_FOOD_STOCK = 20




class Colony:
    """
    a class for representing a Colony
    """
    def __init__(self, ct_ant = 1, food_stock = 20, nest_capacity = 100):
        self.__ctAnt = ct_ant
        self.__ant = []
        self.__nest = Nest(nest_capacity, food_stock)
        self.__queen = Queen(self)

        self.__live = True


        for x in range(self.__ctAnt - 1):
            self.ant.append(Worker(self))

    def manage_ressources(self):
        for ant in self.__ant:
            self.__nest.food_stock -= 1 if ant.role == 'Worker' else 3
        self.__nest.food_stock -= 5
        if self.__nest.food_stock < 0:
            self.destruct_nest()

    def manage_expansion_nest(self):
        if self.__ctAnt == self.__nest.ant_capacity and randint(0, 100) > 10:
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


class Ant:
    """
    a class for representing an Ant
    """
    def __init__(self, role):
        self.position = [0, 0]
        self.role = role

    def do(self):
        pass

    def detect_pheromone(self):
        pass

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

    def find_food(self):
        pass

    def drop_food(self):
        pass


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
            self.food_stock += 1

    def upgrade(self):
        self.ant_capacity += NEST_EXPANSION_RATE
        self.food_capacity += NEST_EXPANSION_RATE
        self.level += 1


def run():
    colony = Colony()
    while colony.live:

        #colony.manage_ressources()
        #colony.manage_expansion_nest()
        colony.queen.lay_eggs()
        print(len(colony.ant))

        sleep(0.1)


if __name__ == '__main__':
    run()

