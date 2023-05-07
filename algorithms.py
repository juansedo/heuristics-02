from typing import Callable

from utils import compare_plot, real_objective_func as Z
from problem import Problem
import time

def VND(problem: Problem, initial_solution: Callable[[], dict]):
    j = 0
    first_solution, initial_time = initial_solution()
    best_solution = first_solution
    
    hoods = [
        problem.swapping,
        problem.external_swapping,
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
    first_solution, initial_time = initial_solution()
    best_solution = first_solution
    sol = first_solution
    
    hoods = [
        problem.swapping,
        problem.external_swapping,
        problem.insertion,
        problem.reversion,
    ]

    start = time.time()
    for i in range(nsol):
        failed_iterations = 0
        best_local_solution = sol
        while failed_iterations < 2:
            j = 0
            disturbed_solution = problem.shuffle(best_local_solution)
            best_local_solution = disturbed_solution
            while j < len(hoods):
                best_neighbor = hoods[j](best_local_solution)
                if problem.Z(best_neighbor) < problem.Z(best_local_solution):
                    j = 0
                    best_local_solution = best_neighbor
                else:
                    j += 1
            
            #print(f'{problem.Z(best_local_solution)} < {problem.Z(best_solution)} || {failed_iterations}')
            if problem.Z(best_local_solution) < problem.Z(best_solution):
                best_solution = best_local_solution
            else:
                failed_iterations += 1
        best_local_solution = initial_solution()

    final_time = time.time() - start

    initial_Z = problem.Z(first_solution)
    final_Z = problem.Z(best_solution)
    return best_solution, [first_solution, round(initial_Z, 2), round(initial_time, 2)], [best_solution, round(final_Z, 2), round(final_time, 2)]
