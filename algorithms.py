from typing import Callable

from utils import real_objective_func as Z
from problem import Problem
import time
import math
import random

def VND(problem: Problem, initial_solution: Callable[[], dict]):
    j = 0
    first_solution, initial_time = initial_solution()
    best_solution = first_solution
    
    hoods = [
        problem.swapping,
        problem.external_swapping,
        problem.external_insertion,
        problem.insertion,
        problem.reversion,
    ]

    start = time.time()
    while j < len(hoods):
        best_neighbor = hoods[j](best_solution)
        if problem.Z(best_neighbor) < problem.Z(best_solution):
            j = 0
            best_solution = best_neighbor
        else:
            j += 1
    final_time = time.time() - start

    initial_Z = problem.Z(first_solution)
    final_Z = problem.Z(best_solution)
    return best_solution, [first_solution, round(initial_Z, 2), round(initial_time, 2)], [best_solution, round(final_Z, 2), round(final_time, 2)]


# Multistart, Perturbed, Simulated Annealing
def MS_ILS(problem: Problem, initial_solution, nsol = 5, T_init = 100, r = 0.7):
    first_solution, initial_time = initial_solution()
    best_solution = first_solution
    
    hoods = [
        problem.swapping,
        problem.external_swapping,
        problem.external_insertion,
        problem.insertion,
    ]

    start = time.time()
    for i in range(nsol):
        failed_iterations = 0
        best_local_solution, i_time = initial_solution()
        while failed_iterations < 2:
            j = 0
            disturbed_solution = problem.shuffle(best_local_solution)
            best_local_solution = disturbed_solution

            T = T_init
            L = 6
            while T > 20:
                l = 0
                while l < L:
                    l += 1
                    sol = hoods[0](best_local_solution)
                    best_neighbor = sol
                    for j in range(1, len(hoods)):
                        sol = hoods[j](best_local_solution)
                        if problem.Z(sol) < problem.Z(best_neighbor):
                            best_neighbor = sol

                    difference = problem.Z(best_local_solution) - problem.Z(best_neighbor)
                    if difference < 0:
                        best_local_solution = best_neighbor
                        if problem.Z(best_local_solution) < problem.Z(best_solution):
                            best_solution = best_local_solution
                            break
                    elif random.random() < 1/math.exp(difference/T):
                        best_local_solution = best_neighbor
                T = T*r
            if problem.Z(best_local_solution) < problem.Z(best_solution):
                best_solution = best_local_solution
            else:
                failed_iterations += 1
    final_time = time.time() - start

    initial_Z = problem.Z(first_solution)
    final_Z = problem.Z(best_solution)
    return best_solution, [first_solution, round(initial_Z, 2), round(initial_time, 2)], [best_solution, round(final_Z, 2), round(final_time, 2)]
