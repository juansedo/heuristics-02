from typing import Callable, List

from utils import objective_func as Z


def VND(hood_callback: Callable[[List], List]):
    j = 0
    solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    neighbours = hood_callback(solution)

    while j < len(neighbours):
        solution_aux = neighbours[j]
        if Z(solution_aux) < Z(solution):
            j = 0
            solution = solution_aux
            neighbours = hood_callback(solution)
        else:
            j += 1
    print(f"{solution}, Z: {Z(solution)}")
    return solution