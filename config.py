QUANTITY_FOOD_FOR_LAYING_EGG = 10
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 100
NEST_START_FOOD_STOCK = 50
NEST_START_CAPACITY = 15
MAX_SOLDIER_FOR_WORKER = 50 # 0...100 the max soldier per worker in %
WORKER_DAMAGE = 1
SOLDIER_DAMAGE = 3
PROBABILITY_TO_LAY_EGG = 25 # 0...100

def algo_laying_egg(colony):
    nb_of_soldier = len([ant for ant in colony.ant if ant.role == 'soldier'])
    max_soldier = nb_of_soldier * MAX_SOLDIER_FOR_WORKER / 100
    can_lay = len(colony.ant) > QUANTITY_ANT_FOR_LAYING_SOLDIER
    can_lay_soldier = nb_of_soldier < max_soldier
    return can_lay and can_lay_soldier