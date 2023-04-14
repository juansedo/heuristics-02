import random

import hoods
from algorithms import ILS, MS_ILS, VND
from utils import objective_func


def initial_solution():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def initial_solution_rand():
    solutions = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 2, 1, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        [0, 1, 7, 3, 4, 6, 5, 2, 8, 9],
    ]
    return list(random.choice(solutions))

def shuffle(array):
    arr = array.copy()
    random.shuffle(arr)
    return arr

solution = MS_ILS(5, initial_solution_rand, hoods.v1, shuffle)
print(f"{solution}, Z: {objective_func(solution)}")