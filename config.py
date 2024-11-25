QUANTITY_FOOD_FOR_LAYING_EGG = 10
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 100
NEST_START_FOOD_STOCK = 50
NEST_START_CAPACITY = 15
MAX_SOLDIER_FOR_WORKER = 50 # 0...100 the max soldier per worker in %
WORKER_DAMAGE = 1
SOLDIER_DAMAGE = 3
PROBABILITY_TO_LAY_EGG = 25 # 0...100
LIFE_BY_ROLE = {'worker': 250, 'soldier': 500, 'queen': 10000}
PROBABILITY_TO_FIND_FOOD = 10
QT_FOOD_EAT_BY_ROLE = {'worker': 1, 'soldier': 2, 'queen': 5}
PROBABILITY_TO_EXPAND_NEST_WHEN_NEST_ALMOST_FULL = 10

def algo_laying_egg(colony):
    nb_of_worker = len([ant.role for ant in colony.ant if ant.role == 'worker'])
    nb_of_soldier = len([ant for ant in colony.ant if ant.role == 'soldier'])
    max_soldier = (nb_of_worker * MAX_SOLDIER_FOR_WORKER / 100) + 1
    can_lay = len(colony.ant) > QUANTITY_ANT_FOR_LAYING_SOLDIER
    can_lay_soldier = nb_of_soldier < max_soldier
    return can_lay and can_lay_soldier