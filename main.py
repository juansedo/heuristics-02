import random

from algorithms import MS_ILS, VND, RVNS
from utils import generate_distance_matrix
from grasp import runGRASP as get_initial
from files import get_test_file
from utils import real_objective_func as Z
import utils
from problem import Problem

def initial_solution_rand():
    solutions = []
    for i in range(3):
        solutions.append(initial_solution())
    return list(random.choice(solutions))


def main():
    headers, data = get_test_file(8)
    n, R, Q, Th = headers
    distance_matrix, demands = generate_distance_matrix(data, n)
    
    problem = Problem(distance_matrix, demands, n, R, Q, Th, data)

    def initial_solution():
        paths, distances, total_time = get_initial(n, R, Q, Th, data)
        return paths

    best_sol = VND(problem, initial_solution)
    #best_sol = RVNS(problem, initial_solution)
    #best_sol = MS_ILS(problem, initial_solution)

if __name__ == "__main__":
    main()
