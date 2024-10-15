from random import randint


class Colony:
    """
    a class for representing a Colony
    """
    def __init__(self, ct_ant, food_stock):
        self.ctAnt = ct_ant
        self.food_stock = food_stock

    def manage_ressources(self):
        pass

    def manage_expansion_nest(self):
        pass

    def react_to_menace(self):
        pass


class Ant:
    """
    a class for representing a Ant
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


class Queen(Ant):
    """
    a class for representing the unique queen
    """
    def __init__(self):
        super().__init__('queen')
        pass

    def lay_eggs(self):
        pass


class Worker(Ant):
    """
    class for representing an ant of type worker
    """
    def __init__(self):
        super().__init__('worker')
        pass

    def find_food(self):
        pass

    def drop_food(self):
        pass


class Soldier(Ant):
    """
        class for representing an ant of type soldier
        """
    def __init__(self):
        super().__init__('soldier')
        pass

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
    a class for representing a nest
    """
    def __init__(self, capacity):
        self.capacity = capacity

    def stock_food(self):
        pass



ant_dict = []
for x in range(50):
    ant = Worker()
    ant.position = [randint(0, 100), randint(0, 100)]
    ant.x += 200
    ant.y += 100
    ant_dict.append(ant)

for x in ant_dict:
    print(x.role, x.x, x.y)