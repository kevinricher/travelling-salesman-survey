from tsp_solver import TSP_Solver
from tsp_plot import plot_tour
import time


def main():
    print("Running main:")
    solver = TSP_Solver(100, 11)
    t0 = time.clock()
    brute_force_solution = solver.brute_force()
    t1 = time.clock()
    brute_force_solution_length = TSP_Solver.tour_length(brute_force_solution)
    print("Brute force solution: {}.".format(brute_force_solution))
    print("Brute force solution length: {}.".format(brute_force_solution_length))
    print("Found tour by brute force in {:.3f} seconds.".format(t1-t0))
    # plot_tour(brute_force_solution)

    t0 = time.clock()
    nn_solution = solver.nearest_neighbour()
    t1 = time.clock()
    nn_solution_length = solver.tour_length(nn_solution)
    print("Nearest neighbour solution: {}.".format(nn_solution))
    print("Nearest neighbour solution length: {}.".format(
        nn_solution_length))
    print("Found tour by nearest neighbour in {:.3f} seconds.".format(t1-t0))
    # plot_tour(nn_solution)

    t0 = time.clock()
    altered_nn_solution = solver.altered_nearest_neighbour()
    t1 = time.clock()
    altered_nn_solution_length = solver.tour_length(altered_nn_solution)
    print("Nearest neighbour solution: {}.".format(altered_nn_solution))
    print("Nearest neighbour solution length: {}.".format(
        altered_nn_solution_length))
    print(
        "Found tour by altered nearest neighbour in {:.3f} seconds.".format(t1-t0))
    # plot_tour(nn_solution)


if (__name__ == "__main__"):
    main()
else:
    print(__name__)
