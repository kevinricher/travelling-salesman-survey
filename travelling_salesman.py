from tsp_solver import TSP_Solver
from tsp_plot import plot_tour, plot_4_tours
from matplotlib import pyplot as plt
import time


def main():
    print("Running main:")
    solver = TSP_Solver(100, 10, 3)

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
    # print("Nearest neighbour solution: {}.".format(nn_solution))
    print("Nearest neighbour solution length: {}.".format(
        nn_solution_length))
    print("Found tour by nearest neighbour in {:.3f} seconds.".format(t1-t0))
    # plot_tour(nn_solution)

    t0 = time.clock()
    repeated_nn_solution = solver.repeated_nearest_neighbour()
    t1 = time.clock()
    repeated_nn_solution_length = solver.tour_length(repeated_nn_solution)
    # print("Repeated nearest neighbour solution: {}.".format(repeated_nn_solution))
    print("Repeated nearest neighbour solution length: {}.".format(
        repeated_nn_solution_length))
    print(
        "Found tour by repeated nearest neighbour in {:.3f} seconds.".format(t1-t0))
    # plot_tour(repeated_nn_solution)

    t0 = time.clock()
    altered_nn_solution = solver.altered_nearest_neighbour()
    t1 = time.clock()
    altered_nn_solution_length = solver.tour_length(altered_nn_solution)
    print("Altered nearest neighbour solution: {}.".format(altered_nn_solution))
    print("Altered nearest neighbour solution length: {}.".format(
        altered_nn_solution_length))
    print(
        "Found tour by altered nearest neighbour in {:.3f} seconds.".format(t1-t0))
    # plot_tour(altered_nn_solution)

    plot_4_tours(brute_force_solution, nn_solution,
                 repeated_nn_solution, altered_nn_solution)
    plt.show()


if (__name__ == "__main__"):
    main()
else:
    print(__name__)
