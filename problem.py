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
        
    def _handle_solution(self, solution: dict, transformer, rand: bool = False):
        truck = 0
        truck_offset = 1
        best_solution = {}
        hood = []

        i = 1
        j = 1

        while truck_offset < len(solution):
            if (i < len(solution[truck_offset]) - 1 and solution[truck_offset][i] == 0): i += 1
            if (j < len(solution[truck_offset]) - 1 and solution[truck_offset][j] == 0): j += 1
            if (j >= len(solution[truck_offset]) - 1):
                i += 1
                j = 1
            if (i >= len(solution[truck]) - 1):
                truck_offset += 1
                i = 1
                j = 1
                continue
            new_sol = transformer(solution, truck, truck_offset, i, j)
            
            if self.check_consistency_solution(new_sol):
                hood.append(new_sol)
            j += 1

        if len(hood) > 0:
            if rand: best_solution = random.choice(hood)
            else: best_solution = self.get_optimal_solution(hood)
        else:
            best_solution = solution
        return best_solution
    
    def _external_swapping(self, solution, truck, truck_offset, i, j):
        try:
            new_sol = copy.deepcopy(solution)
            elem1 = new_sol[truck][i]
            new_sol[truck][i] = new_sol[truck_offset][j]
            new_sol[truck_offset][j] = elem1
            return new_sol
        except:
            print(f'WARNING: ({truck},{truck_offset},{i},{j}) ON')
            print(solution)
            return solution
    
    def _external_insertion(self, solution, truck, truck_offset, i, j):
        new_sol = copy.deepcopy(solution)
        new_sol[truck_offset].insert(j, new_sol[truck].pop(i))
        return new_sol

    def external_swapping(self, solution: dict, rand: bool = False):
        return self._handle_solution(solution, self._external_swapping, rand)
    
    def external_insertion(self, solution: dict, rand: bool = False):
        return self._handle_solution(solution, self._external_insertion, rand)


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
        shuffled_solution = copy.deepcopy(solution)
        trucks = len(shuffled_solution)
        
        for i in range(5):
            try:
                nodes_to_steal = random.randint(1, 3)
                path1 = random.randint(0, trucks - 1)
                path2 = random.randint(0, trucks - 1)

                if len(shuffled_solution[path1]) <= nodes_to_steal + 2: continue
                lb = random.randint(1, len(shuffled_solution[path1]) - 1 - nodes_to_steal)
                nodes = shuffled_solution[path1][lb:lb + nodes_to_steal]
                shuffled_solution[path1] = shuffled_solution[path1][:lb] + shuffled_solution[path1][lb + nodes_to_steal:]
                lb = random.randint(1, len(shuffled_solution[path2]) - 1)
                shuffled_solution[path2] = shuffled_solution[path2][:lb] + nodes + shuffled_solution[path2][lb:]
            except:
                pass
        
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

    def check_consistency(self, path: list):
        amount = self.Q
        for i in range(len(path) - 1):
            actualNode, nextNode = [path[i], path[i + 1]]
            if actualNode == 0: amount = self.Q
            if nextNode == 0: continue
            amount -= self.demands[nextNode]
            if amount < 0:
                return False
        return True

    def check_consistency_solution(self, solution: dict):
        values: List[bool] = [self.check_consistency(path) for path in solution.values()]
        return all(values)

    def calculate_path_distance(self, path: list):
        return sum([self.distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1)])
    
    def get_distance_array(self, solution: dict):
        return [self.calculate_path_distance(path) for path in solution.values()]
    
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
