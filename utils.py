from typing import List
import matplotlib.pyplot as plt
import numpy as np
import math
import os

def rimraf(folder_path):
    if len(os.listdir(folder_path)) > 0:
        answer = input(f"There are files on the {folder_path} folder, are you sure to delete them? (Y/n): ")
        if answer == "n" or answer == "N":
            print("Files will not be to deleted")
            return
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print("Files deleted successfully")


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
    return calculate_path_distance(distance_matrix, path) <= Th


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


def compare_plot(method, title, data, initial_sol, final_sol, index):
    paths1, initial_Z, initial_time = initial_sol
    paths2, final_Z, final_time = final_sol
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    fig.suptitle(title, fontsize=16)

    ax1.title.set_text(f'Before ({round(initial_time, 2)} s)')
    ax1.set_xlabel(f'Z: {round(initial_Z, 2)}', fontweight='bold', fontsize=14)

    ax2.title.set_text(f'After ({round(final_time, 2)} s)')
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

    save_plot(fig, f"{method}-mtVRP{index}")


def summary_time_plot(filename, labels, total_times = None):
    if (len(labels) == 0 or len(total_times) == 0): return
    
    plt.clf()
    fig = plt.gcf()
    ax = plt.gca()

    size = np.arange(len(labels))
    width = 0.3
    if ('VND' in total_times):
        bar1 = ax.bar(size - width/2, total_times['VND'], width, label='VND')
        ax.bar_label(bar1)
    if ('MS_ILS' in total_times):
        bar2 = ax.bar(size + width/2, total_times['MS_ILS'], width, label='MS_ILS')
        ax.bar_label(bar2)

    ax.set_ylabel('Compute time (seconds)')
    ax.set_title('Algorithms comparison')
    ax.set_xticks(size, labels)
    ax.legend(loc='upper left', ncols=1)
    
    fig.set_size_inches(12.5, 5.5)
    fig.set_dpi(90)
    save_plot(fig, filename)


def summary_plot(filename, data):
    plt.clf()
    fig = plt.gcf()
        
    xitems = []
    yitems = []
    plt.plot(BKS.get_labels(), BKS.get_list(), color="C2")
    plt.fill_between(BKS.get_labels(), BKS.get_list(), color="C2", alpha=0.3)
    for key, value in data.items():
        xitems = [item[0] for item in value]
        yitems = [item[1] for item in value]
        plt.plot(xitems, yitems, label=key, marker='o')
        for i in range(len(xitems)):
            plt.annotate(str(round(yitems[i], 2)), (xitems[i], yitems[i] * 1.05))

    plt.legend(loc='upper left', ncols=1)
    fig.set_size_inches(12.5, 5.5)
    fig.set_dpi(90)
    save_plot(fig, filename)
