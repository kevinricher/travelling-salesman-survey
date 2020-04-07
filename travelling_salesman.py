from tsp_solver import TSP_Solver
from tsp_plot import plot_tour
import time


def main():
    print("Running main:")
    solver = TSP_Solver(100, 9)
    t0 = time.clock()
    brute_force_solution = solver.brute_force()
    t1 = time.clock()
    brute_force_solution_length = TSP_Solver.tour_length(brute_force_solution)
    print(brute_force_solution)
    print(brute_force_solution_length)
    print("Time 1: {}, time 2: {}".format(t0, t1))
    print("Found tour by brute force in {:.3f} seconds.".format(t1-t0))
    # plot_tour(brute_force_solution)

    print(type(set(solver.instance.points)))
    print(type({solver.first(solver.instance.points)}))
    print(type(set(solver.instance.points) -
               {solver.first(solver.instance.points)}))
    print((set(solver.instance.points) -
           {solver.first(solver.instance.points)}))
    print(type(solver.instance.points))
    print(solver.instance.points)
    print(type(solver.first(solver.instance.points)))
    print(type([solver.first(solver.instance.points)]))

    t0 = time.clock()
    nn_solution = solver.nearest_neighbour()
    t1 = time.clock()
    nn_solution_length = solver.tour_length(nn_solution)
    print("Found tour by nearest neighbour in {:.3f} seconds.".format(t1-t0))
    plot_tour(nn_solution)


if __name__ == "__main__":
    main()
else:
    print(__name__)
