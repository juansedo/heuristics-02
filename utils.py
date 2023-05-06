from typing import List
import matplotlib.pyplot as plt
import numpy as np
import math
import os

# MOCK FUNCTIONS
def objective_func(array):
    return array[0] + array[5] + array[9]


def factible_func(array):
    return True


# STRATEGIES
def get_optimal(distance_matrix, demands, Q, Th, solutions):
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


class BKS:
    mtVRP1 = 546.29
    mtVRP2 = 835.80
    mtVRP3 = 858.58
    mtVRP4 = 866.58
    mtVRP5 = 829.45
    mtVRP6 = 826.14
    mtVRP7 = 1034.61
    mtVRP8 = 1300.02
    mtVRP9 = 1300.62
    mtVRP10 = 1078.64
    mtVRP11 = 845.48
    mtVRP12 = 823.14
    
    def get_labels():
        return [
            "mtVRP1",
            "mtVRP2",
            "mtVRP3",
            "mtVRP4",
            "mtVRP5",
            "mtVRP6",
            "mtVRP7",
            "mtVRP8",
            "mtVRP9",
            "mtVRP10",
            "mtVRP11",
            "mtVRP12",
        ]
    
    def get_list():
        return [
            BKS.mtVRP1,
            BKS.mtVRP2,
            BKS.mtVRP3,
            BKS.mtVRP4,
            BKS.mtVRP5,
            BKS.mtVRP6,
            BKS.mtVRP7,
            BKS.mtVRP8,
            BKS.mtVRP9,
            BKS.mtVRP10,
            BKS.mtVRP11,
            BKS.mtVRP12,
        ]


def save_plot(fig, title):
    if os.path.exists('./outputs') == False:
        os.mkdir('./outputs')
    
    filename = title + ".png"
    path_plot = './outputs/' + filename
    fig.savefig(path_plot, dpi=fig.dpi)


def compare_plot(title, data, initial_sol, final_sol, index):
    paths1, initial_Z = initial_sol
    paths2, final_Z = final_sol 
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    fig.suptitle(title, fontsize=16)

    ax1.title.set_text('Before')
    ax1.set_xlabel(f'Z: {round(initial_Z, 2)}', fontweight='bold', fontsize=14)

    ax2.title.set_text('After')
    ax2.set_xlabel(f'Z: {round(final_Z, 2)}', fontweight='bold', fontsize=14)
    
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

    #plt.show()
    save_plot(fig, f"VND in mtVRP{index}")

def summary_plot(filename, data):
    plt.clf()
    fig = plt.gcf()
        
    xitems = []
    yitems = []
    plt.plot(BKS.get_labels(), BKS.get_list(), color="C1")
    plt.fill_between(BKS.get_labels(), BKS.get_list(), color="C1", alpha=0.3)
    for key, value in data.items():
        xitems = [item[0] for item in value]
        yitems = [item[1] for item in value]
        plt.plot(xitems, yitems, label=key, marker='o')
        for i in range(len(xitems)):
            plt.annotate(str(round(yitems[i], 2)), (xitems[i], yitems[i] * 1.05))
    #plt.show()
    fig.set_size_inches(12.5, 5.5)
    fig.set_dpi(90)
    save_plot(fig, filename)