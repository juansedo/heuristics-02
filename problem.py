from typing import List
import random
import copy

class Problem:
    def __init__(self, distance_matrix, demands, n, R, Q, Th, data):
        self.distance_matrix = distance_matrix
        self.demands = demands
        self.n = n
        self.R = R
        self.Q = Q
        self.Th = Th
        self.data = data

    def external_swapping(self, solution: dict, rand: bool = False):
        truck = 0
        truck_offset = 1
        best_solution = {}
        hood = []

        while truck_offset < len(solution):
            i = 1
            j = 1
            while True:
                if (i < len(solution[truck]) - 1 and solution[truck][i] == 0): i += 1
                if (j < len(solution[truck_offset]) - 1 and solution[truck_offset][j] == 0): j += 1
                if (i >= len(solution[truck]) - 1) and (j >= len(solution[truck_offset]) - 1):
                    truck_offset += 1
                    break
                
                new_sol = copy.deepcopy(solution)
                elem1 = new_sol[truck][i]
                elem2 = new_sol[truck_offset][j]
                new_sol[truck][i] = elem2
                new_sol[truck_offset][j] = elem1
                
                if self.check_consistency_solution(new_sol):
                    hood.append(new_sol)
                if (j >= len(solution[truck_offset]) - 1):
                    i += 1
                    j = 1
                else: j += 1


        if len(hood) > 0:
            if rand: best_solution = random.choice(hood)
            else: best_solution = self.get_optimal_solution(hood)
        else:
            best_solution = solution
        return best_solution


    def swapping(self, solution: dict, rand: bool = False):
        truck = 0
        best_solution = {}
        for sol in solution.values():
            hood = []
            for i in range(1, len(sol) - 2):
                for j in range(i + 1, len(sol) - 1):
                    neighbor = sol.copy()
                    aux = neighbor[i]
                    neighbor[i] = neighbor[j]
                    neighbor[j] = aux
                    hood.append(neighbor)
            hood = list(filter(lambda x: self.check_consistency(x), hood))
            if len(hood) > 0:
                if rand: best_solution[truck] = random.choice(hood)
                else: best_solution[truck] = self.get_optimal(hood)
            else:
                best_solution[truck] = sol
            truck += 1
        return best_solution
    
    def insertion(self, solution: dict, rand: bool = False):
        truck = 0
        best_solution = {}
        for sol in solution.values():
            hood = []
            for i in range(1, len(sol) - 2):
                for j in range(i + 1, len(sol) - 1):
                    neighbor = sol.copy()
                    neighbor.insert(i, neighbor.pop(j))
                    hood.append(neighbor)
            hood = list(filter(lambda x: self.check_consistency(x), hood))
            if len(hood) > 0:
                if rand: best_solution[truck] = random.choice(hood)
                else: best_solution[truck] = self.get_optimal(hood)
            else:
                best_solution[truck] = sol
            truck += 1
        return best_solution

    def reversion(self, solution: dict, rand: bool = False):
        truck = 0
        best_solution = {}
        for sol in solution.values():
            hood = []
            for i in range(1, len(sol) - 2):
                for j in range(i + 1, len(sol) - 1):
                    neighbor = sol.copy()
                    neighbor[i:j] = neighbor[i:j][::-1]
                    hood.append(neighbor)
            hood = list(filter(lambda x: self.check_consistency(x), hood))
            if len(hood) > 0:
                if rand: best_solution[truck] = random.choice(hood)
                else: best_solution[truck] = self.get_optimal(hood)
            else:
                best_solution[truck] = sol
            truck += 1
        return best_solution
    
    def shuffle(self, solution: dict):
        truck = 0
        shuffled_solution = {}
        for s in solution.values():
            arr = s.copy()
            arr = arr[1:-1]
            random.shuffle(arr)
            shuffled_solution[truck] = [0] + arr + [0]
            truck += 1
        return shuffled_solution


    def get_optimal(self, possible_paths: list):
        optimal = possible_paths[0]
        for path in possible_paths:
            if self.calculate_path_distance(path) < self.calculate_path_distance(optimal):
                optimal = path
        return optimal

    def get_optimal_solution(self, solutions: List[dict]):
        optimal = solutions[0]
        for sol in solutions:
            if self.Z(sol) < self.Z(optimal):
                optimal = sol
        return optimal

    # Check consistency
    def check_consistency(self, path: list):
        amount = self.Q
        for i in range(len(path) - 1):
            actualNode, nextNode = [path[i], path[i + 1]]
            if actualNode == 0: amount = self.Q
            if nextNode == 0: continue
            amount -= self.demands[nextNode]
            if amount < 0:
                #print(f'|--Inconsistency in path {path} on position {i}')
                return False
        return True

    def check_consistency_solution(self, solution: dict):
        values: List[bool] = [self.check_consistency(path) for path in solution.values()]
        return all(values)

    def calculate_path_distance(self, path: list):
        return sum([self.distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1)])
    
    def calculate_lower_bound(self):
        sol = []
        for i in range(self.n + 1):
            s = self.distance_matrix[i][i:(self.n + 1)]
            sol.append(s)
        return sum(sol)

    # objective function
    def Z(self, solution: dict):
        total = 0
        for path in solution.values():
            value = self.calculate_path_distance(path)
            total += round(value, 2)
        return total
