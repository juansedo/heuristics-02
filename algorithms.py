import random
from typing import Callable, List

from utils import compare_plot, real_objective_func as Z
from problem import Problem
import time

def VND(problem: Problem, initial_solution: Callable[[], dict]):
    j = 0
    first_solution = initial_solution()
    best_solution = first_solution
    initial_Z = problem.Z(best_solution)
    
    hoods = [
        problem.swapping,
        problem.external_swapping,
        problem.insertion,
        problem.reversion,
    ]

    while j < len(hoods):
        best_neighbor = hoods[j](best_solution)

        if problem.Z(best_neighbor) < problem.Z(best_solution):
            j = 0
            best_solution = best_neighbor
        else:
            j += 1

    final_Z = problem.Z(best_solution)
    return best_solution, [first_solution, initial_Z], [best_solution, final_Z]


def RVNS(problem: Problem, initial_solution: Callable[[], dict], t_max = 10):
    j = 0
    first_solution = initial_solution()
    best_solution = first_solution
    print(f'Z: {problem.Z(best_solution)}')

    start = time.time()
    end = start
    while end - start < t_max:
        while j < 3:
            if j == 0: best_neighbor = problem.swapping(best_solution, rand=True)
            elif j == 1: best_neighbor = problem.insertion(best_solution, rand=True)
            elif j == 2: best_neighbor = problem.reversion(best_solution, rand=True)

            if problem.Z(best_neighbor) < problem.Z(best_solution):
                j = 0
                best_solution = best_neighbor
            else:
                j += 1
        end = time.time()

    print(f'Z: {problem.Z(best_solution)}')
    compare_plot(problem.data, first_solution, best_solution)
    return best_solution

# Multistart, Perturbed, Threshold Acceptance
def MS_ILS(problem: Problem, initial_solution, nsol = 5):
    solution = initial_solution()
    first_solution = solution
    best_solution = solution
    print(f'Z: {problem.Z(best_solution)}')
    for i in range(nsol):
        failed_iterations = 0
        best_local_solution = solution
        while failed_iterations < 10:
            j = 0
            disturbed_solution = problem.shuffle(best_solution)
            while j < 3:
                if j == 0: best_neighbor = problem.swapping(disturbed_solution)
                elif j == 1: best_neighbor = problem.insertion(disturbed_solution)
                elif j == 2: best_neighbor = problem.reversion(disturbed_solution)

                if problem.Z(best_neighbor) < problem.Z(best_local_solution) * 1.01:
                    j = 0
                    best_local_solution = best_neighbor
                else:
                    j += 1
            
            #print(f'Z(disturbed): {problem.Z(disturbed_solution)}, Z(local_best): {problem.Z(best_local_solution)}, Z(best): {problem.Z(best_solution)}')
            if problem.Z(best_local_solution) < problem.Z(best_solution):
                best_solution = best_local_solution
                failed_iterations = 0
            else:
                failed_iterations += 1
        solution = initial_solution()
    print(f'Z: {problem.Z(best_solution)}')
    compare_plot(problem.data, first_solution, best_solution)
    return solution
