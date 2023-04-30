import numpy as np
import math

def swapping(array, i, j):
    arr = array.copy()
    aux = arr[i]
    arr[i] = arr[j]
    arr[j] = aux
    return arr

def reversion(array, i, j):
    arr = array.copy()
    arr[i:(j+1)] = arr[i:(j+1)][::-1]
    return arr

def insertion(array, i, j):
    arr = array.copy()
    arr.insert(i, arr.pop(j))
    return arr

def objective_func(array):
    return array[0] + array[5] + array[9]

def factible_func(array):
    return True




def getDistance(n1, n2):
  x1, y1 = n1
  x2, y2 = n2
  return round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)

def generate_distance_matrix(data, n):
    distances = np.zeros((n + 1, n + 1))
    demands = np.zeros(n + 1)
    for node in data:
        values = [getDistance(node[1:3], node2[1:3]) for node2 in data]
        distances[node[0]] = values
        demands[node[0]] = node[3]
    return [distances, demands]

def calculate_path_factibility(distance_matrix, path, Th):
    if calculate_path_distance(distance_matrix, path) <= Th:
        return True
    else:
        print(f'|--Infactible path {path} with Th = {Th} and distance = {calculate_path_distance(distance_matrix, path)}')
        return False

def calculate_path_consistency(demands, path, Q):
    amount = Q
    for i in range(len(path) - 1):
        actualNode = path[i]
        nextNode = path[i + 1]
        if actualNode == 0: amount = Q
        if nextNode == 0: continue
        amount -= demands[nextNode]
        if amount < 0:
            print(f'|--Inconsistency in path {path} on position {i}')
            return False
    return True

def calculate_path_distance(distance_matrix, path):
    total = 0
    for i in range(len(path) - 1):
        actualNode = path[i]
        nextNode = path[i + 1]
        total += distance_matrix[actualNode][nextNode]
    return round(total, 2)

def real_objective_func(distance_matrix, solution):
    paths, total_distances, total_time = solution
    total = 0
    for path in paths.values():
        total += calculate_path_distance(distance_matrix, path)
    return total

def real_consistency_func(distance_matrix, demands, solution, Q, Th):
    paths, total_distances, total_time = solution
    for path in paths.values():
        calculate_path_factibility(distance_matrix, path, Th)
        calculate_path_consistency(demands, path, Q)
    return True
    