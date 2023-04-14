import random

import hoods
from algorithms import ILS, VND
from utils import objective_func


def initial_solution():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def shuffle(array):
    arr = array.copy()
    random.shuffle(arr)
    return arr

solution = ILS(initial_solution, hoods.v1, shuffle)
print(f"{solution}, Z: {objective_func(solution)}")