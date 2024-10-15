class Colony:
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
    def __init__(self, role):
        self.position = [0, 0]
        self.role = role

    def do(self):
        pass

    def detect_pheromone(self):
        pass


class Queen(Ant):
    def __init__(self):
        super().__init__('queen')
        pass

    def lay_eggs(self):
        pass


class Worker(Ant):
    def __init__(self):
        super().__init__('worker')
        pass

    def find_food(self):
        pass

    def drop_food(self):
        pass


class Soldier(Ant):
    def __init__(self):
        super().__init__('soldier')
        pass

    def defend_nest(self):
        pass


class Pheromone:
    def __init__(self, p_type, intensity):
        self.p_type = p_type
        self.intensity = intensity

    def dispel(self):
        self.intensity =- 1


class Nest:
    def __init__(self, capacity):
        self.capacity = capacity

    def stock_food(self):
        pass

