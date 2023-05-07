import random
import argparse

from algorithms import VND, MS_ILS
from utils import generate_distance_matrix, rimraf
from grasp import runGRASP as get_initial
from files import get_test_file, Slides
from utils import compare_plot, summary_time_plot
from problem import Problem

def initial_solution_rand():
    solutions = []
    for i in range(3):
        solutions.append(initial_solution())
    return list(random.choice(solutions))

def solve(method, index):
    headers, data = get_test_file(index)
    n, R, Q, Th = headers
    distance_matrix, demands = generate_distance_matrix(data, n)
    
    problem = Problem(distance_matrix, demands, n, R, Q, Th, data)

    def initial_solution():
        paths, distances, total_time = get_initial(n, R, Q, Th, data)
        return paths, total_time

    if (method == "VND"):
        best_sol, initial, final = VND(problem, initial_solution)
        compare_plot("VND", "VND in mtVRP" + str(index), problem.data, initial, final, index)
        print(f'Instance mtVRP{index} (VND) -> Z: {final[1]} ({final[2]} s)')
    elif (method == "MS_ILS"):
        best_sol, initial, final = MS_ILS(problem, initial_solution)
        compare_plot("MS_ILS", "MS_ILS in mtVRP" + str(index), problem.data, initial, final, index)
        print(f'Instance mtVRP{index} (MS_ILS) -> Z: {final[1]} ({final[2]} s)')
    
    return [final[1], final[2]]

def main():
    parser = argparse.ArgumentParser(description= "Heuristics local search algorithms (by juansedo)")
    parser.add_argument("-f", "--file", nargs="+", type=int, help="File id to read the data from")
    parser.add_argument("-p", "--no-pptx", action="store_true", help="Disable the pptx file generation")
    args = parser.parse_args()
    if (args.file): args.file = list(set(args.file))

    slides = Slides("Local search results", "Presented by: Juan Sebastián Díaz Osorio")

    rimraf('./outputs/')

    iterator = args.file if args.file else range(1, 13)
    for i in iterator:
        best_solution = solve("VND", i)
        slides.add_method_slide("VND", i)
        slides.add_method_value("VND", f"mtVRP{i}", best_solution)
        best_solution = solve("MS_ILS", i)
        slides.add_method_slide("MS_ILS", i)
        slides.add_method_value("MS_ILS", f"mtVRP{i}", best_solution)
    if (args.file is None or len(args.file) > 1):
        slides.generate_timeplot()
    slides.generate_summary()

    if (args.no_pptx == False):
        slides.save('Local Search Report.pptx')

if __name__ == "__main__":
    main()
