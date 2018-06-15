from random import randint, random
from datetime import datetime

def random_number_0_to_1():
    return random()


def random_number_1_to_10():
    return randint(0, 10)

def rand_unique_value():
    return str(random_number_0_to_1()) + str(datetime.now())


print(random_number_0_to_1())
print(random_number_1_to_10())
print(rand_unique_value())
