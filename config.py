QUANTITY_FOOD_FOR_LAYING_EGG = 10
QUANTITY_ANT_FOR_LAYING_SOLDIER = 50
NEST_EXPANSION_RATE = 100
NEST_START_FOOD_STOCK = 50
NEST_START_CAPACITY = 15
MAX_SOLDIER_FOR_WORKER = 50 # 0...100 the max soldier per worker in %
WORKER_DAMAGE = 1
SOLDIER_DAMAGE = 3

def algo_laying_egg(colony):
    return len(colony.ant) > QUANTITY_ANT_FOR_LAYING_SOLDIER and len([ant for ant in colony.ant if ant.role == 'soldier']) < len([ant for ant in colony.ant if ant.role == 'worker']) * MAX_SOLDIER_FOR_WORKER / 100