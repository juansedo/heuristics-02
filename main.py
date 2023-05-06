import random
import argparse

from algorithms import MS_ILS, VND, RVNS
from utils import generate_distance_matrix
from grasp import runGRASP as get_initial
from files import get_test_file, Slides
from utils import compare_plot
from problem import Problem

def initial_solution_rand():
    solutions = []
    for i in range(3):
        solutions.append(initial_solution())
    return list(random.choice(solutions))

def solve(index):
    headers, data = get_test_file(index)
    n, R, Q, Th = headers
    distance_matrix, demands = generate_distance_matrix(data, n)
    
    problem = Problem(distance_matrix, demands, n, R, Q, Th, data)

    def initial_solution():
        paths, distances, total_time = get_initial(n, R, Q, Th, data)
        return paths

    best_sol, initial, final = VND(problem, initial_solution)
    compare_plot("VND in mtVRP" + str(index), problem.data, initial, final, index)
    return final[1]
    #best_sol = RVNS(problem, initial_solution)
    #best_sol = MS_ILS(problem, initial_solution)

def main():
    parser = argparse.ArgumentParser(description= "Heuristics local search algorithms (by juansedo)")
    parser.add_argument("-f", "--file", type=int, help="File id to read the data from")
    parser.add_argument("-p", "--pptx", action="store_true", help="Generate a pptx file with the results")
    args = parser.parse_args()
    print(args)
    
    slides = Slides("Local search results", "Presented by: Juan Sebastián Díaz Osorio")
    
    if (args.file is None):
        for i in range(1, 13):
            best_sol = solve(i)
            slides.add_method_slide("VND", f"VND in mtVRP{i}" + ".png")
            slides.add_method_value("VND", f"mtVRP{i}", best_sol)
        slides.generate_summary()
    else:
        best_sol = solve(args.file)
        slides.add_method_slide("VND", f"VND in mtVRP{args.file}" + ".png")
        slides.add_method_value("VND", f"mtVRP{args.file}", best_sol)
        slides.generate_summary()
        
    if (args.pptx):        
        slides.save('Local Search Report.pptx')

if __name__ == "__main__":
    main()
