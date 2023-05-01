from typing import List
import matplotlib.pyplot as plt
import numpy as np
import math


# MOCK FUNCTIONS
def objective_func(array):
    return array[0] + array[5] + array[9]


def factible_func(array):
    return True


# STRATEGIES
def get_optimal(distance_matrix, Q, Th, solutions):
    optimal = solutions[0]
    for solution in solutions:
        if real_consistency_func(distance_matrix, demands, solution, Q, Th):
            continue
        if calculate_path_distance(distance_matrix, solution) < calculate_path_distance(
            distance_matrix, optimal
        ):
            optimal = solution
    return optimal


def swapping(distance_matrix, array):
    hood = []
    for i in range(2, len(array) - 1):
        neighbor = array.copy()
        aux = neighbor[1]
        neighbor[1] = neighbor[i]
        neighbor[i] = aux
        hood.append(neighbor)
    best = get_optimal(distance_matrix, hood)
    return best


def reversion(distance_matrix: List[List], Q: int, Th: int, solution: dict):
    best_solution = {}
    i = 0
    for sol in solution.values():
        hood = []
        for j in range(3, len(sol)):
            neighbor = sol.copy()
            neighbor[1:j] = neighbor[1:j][::-1]
            hood.append(neighbor)
        best_solution[i] = get_optimal(distance_matrix, Q, Th, hood)
        i += 1
    return best_solution


def insertion(array, i, j):
    arr = array.copy()
    arr.insert(i, arr.pop(j))
    return arr


# DISTANCE MATRIX
def get_distance(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)


def generate_distance_matrix(data, n):
    distances = np.zeros((n + 1, n + 1))
    demands = np.zeros(n + 1)
    for node in data:
        values = [get_distance(node[1:3], node2[1:3]) for node2 in data]
        distances[node[0]] = values
        demands[node[0]] = node[3]
    return [distances, demands]


# CALCULATIONS
def calculate_path_factibility(distance_matrix, path, Th):
    if calculate_path_distance(distance_matrix, path) <= Th:
        return True
    else:
        print(
            f"|--Infactible path {path} with Th = {Th} and distance = {calculate_path_distance(distance_matrix, path)}"
        )
        return False


def calculate_path_consistency(demands, path, Q):
    amount = Q
    for i in range(len(path) - 1):
        actualNode = path[i]
        nextNode = path[i + 1]
        if actualNode == 0:
            amount = Q
        if nextNode == 0:
            continue
        amount -= demands[nextNode]
        if amount < 0:
            print(f"|--Inconsistency in path {path} on position {i}")
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
    paths = solution
    total = 0
    for path in paths.values():
        total += calculate_path_distance(distance_matrix, path)
    return total


def real_consistency_func(distance_matrix, demands, solution, Q, Th):
    paths = solution
    for path in paths.values():
        is_factible = True  # calculate_path_factibility(distance_matrix, path, Th)
        is_consistent = calculate_path_consistency(demands, path, Q)
        if not is_factible or not is_consistent:
            return False
    return True


def compare_plot(data, paths1, paths2):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    x = []
    y = []
    for node in data:
        x.append(node[1])
        y.append(node[2])
    ax1.plot(x, y, "o", label="Nodos")
    ax2.plot(x, y, "o", label="Nodos")

    for p in paths1:
        x = []
        y = []
        for node in paths1[p]:
            x.append(data[node][1])
            y.append(data[node][2])
        ax1.plot(x, y, "-", label=f"Camión {p+1}")

    for p in paths2:
        x = []
        y = []
        for node in paths2[p]:
            x.append(data[node][1])
            y.append(data[node][2])
        ax2.plot(x, y, "-", label=f"Camión {p+1}")

    plt.show()
