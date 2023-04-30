import random

from algorithms import ILS, MS_ILS, VND
from utils import generate_distance_matrix, real_objective_func, real_consistency_func, objective_func
from grasp import run as get_initial
from files import get_test_file

def shuffle(array):
    arr = array.copy()
    random.shuffle(arr)
    return arr

def runGRASP(n, R, Q, Th, data, iterations = 20, alpha = 0.02):
  best = [None, None, None]
  for i in range(iterations):
    paths, distances, time = get_initial(n, R, Q, Th, alpha, data)
    if best[1] is None or sum(distances) < sum(best[1]):
      best[0] = paths
      best[1] = distances
      best[2] = time
  return best

def initial_solution():
    return runGRASP

def initial_solution_rand():
    solutions = [
        runGRASP(),
        runGRASP(),
        runGRASP(),
    ]
    print(solutions)
    return list(random.choice(solutions))

def main():
    headers, data = get_test_file(1)
    n, R, Q, Th = headers
    
    distance_matrix, demands = generate_distance_matrix(data, n)
    sol = runGRASP(n, R, Q, Th, data)
    print(f'Z: {real_objective_func(distance_matrix, sol)}')
    print('Errors on...')
    real_consistency_func(distance_matrix, demands, sol, Q, Th)
    
    #solution = MS_ILS(5, initial_solution_rand, hoods.v1, shuffle)

if __name__ == "__main__":
    main()