import random
from typing import Callable, List

from utils import objective_func as Z


def VND(initial_solution, hood_callback: Callable[[List], List]):
    j = 0
    solution = initial_solution()
    neighbours = hood_callback(solution)

    while j < len(neighbours):
        solution_aux = neighbours[j]
        if Z(solution_aux) < Z(solution):
            j = 0
            solution = solution_aux
            neighbours = hood_callback(solution)
        else:
            j += 1
    return solution


def RVNS(initial_solution, hood_callback: Callable[[List], List]):
    j = 0
    solution = initial_solution()
    neighbours = random.shuffle(hood_callback(solution))

    while j < len(neighbours):
        solution_aux = neighbours[j]
        if Z(solution_aux) < Z(solution):
            j = 0
            solution = solution_aux
            neighbours = random.shuffle(hood_callback(solution))
        else:
            j += 1
    return solution


def ILS(
    initial_solution, hood_callback, shuffle_callback: Callable[[List], List]
):
    failed_iterations = 0
    solution = initial_solution()
    while failed_iterations < 5:
        disturbed_solution = shuffle_callback(solution)
        best_local_solution = VND(lambda: disturbed_solution, hood_callback)
        if Z(best_local_solution) < Z(solution):
            solution = best_local_solution
            failed_iterations = 0
        else:
            failed_iterations += 1
    return solution
