from tsp_solver import TSP_Solver
from tsp_plot import plot_tour, plot_4_tours
from matplotlib import pyplot as plt
import time
import csv


def main():
    print("Running main:")

    for i in range(15, 16):
        print("Solving for size: {}.".format(i))

        with open('tsp_times_{}.csv'.format(i), 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(['Size', 'BF', 'BNB',
                                 'NN', 'RNN', 'ANN', 'GA'])

        with open('tsp_distances_{}.csv'.format(i), 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(['Size', 'BF', 'BNB',
                                 'NN', 'RNN', 'ANN', 'GA'])

        for j in range(1):
            solver = TSP_Solver(100, i, i*(j+1))

            if i <= 10:
                t0 = time.clock()
                brute_force_solution = solver.brute_force()
                t1 = time.clock()
                brute_force_solution_length = TSP_Solver.tour_length(
                    brute_force_solution)
                # print("Brute force solution: {}.".format(brute_force_solution))
                # print("Brute force solution length: {:.3f}.".format(
                #     brute_force_solution_length))
                BF_time = t1-t0
                # print("Found tour by brute force in {:.3f} seconds.".format(t1-t0))
                # # plot_tour(brute_force_solution)
            else:
                brute_force_solution_length = 'NAN'
                BF_time = 'NAN'

            if i <= 20:
                t0 = time.clock()
                branch_and_bound_solution = solver.branch_and_bound()
                t1 = time.clock()
                branch_and_bound_solution_length = TSP_Solver.tour_length(
                    branch_and_bound_solution)
                # # print("Branch and bound solution: {}.".format(branch_and_bound_solution))
                # print("Branch and bound solution length: {:.3f}.".format(
                #     branch_and_bound_solution_length))
                BNB_time = t1-t0
                # print(
                #     "Found tour by branch and bound in {:.3f} seconds.".format(t1-t0))
            else:
                branch_and_bound_solution_length = 'NAN'
                BNB_time = 'NAN'

            t0 = time.clock()
            nn_solution = solver.nearest_neighbour()
            t1 = time.clock()
            nn_solution_length = solver.tour_length(nn_solution)
            # # print("Nearest neighbour solution: {}.".format(nn_solution))
            # print("Nearest neighbour solution length: {:.3f}.".format(
            #     nn_solution_length))
            NN_time = t1-t0
            # print(
            #     "Found tour by nearest neighbour in {:.3f} seconds.".format(t1-t0))
            # # plot_tour(nn_solution)

            t0 = time.clock()
            repeated_nn_solution = solver.repeated_nearest_neighbour()
            t1 = time.clock()
            repeated_nn_solution_length = solver.tour_length(
                repeated_nn_solution)
            # # print("Repeated nearest neighbour solution: {}.".format(repeated_nn_solution))
            # print("Repeated nearest neighbour solution length: {:.3f}.".format(
            #     repeated_nn_solution_length))
            RNN_time = t1-t0
            # print(
            #     "Found tour by repeated nearest neighbour in {:.3f} seconds.".format(t1-t0))
            # # plot_tour(repeated_nn_solution)

            t0 = time.clock()
            altered_nn_solution = solver.altered_nearest_neighbour()
            t1 = time.clock()
            altered_nn_solution_length = solver.tour_length(
                altered_nn_solution)
            # # print("Altered nearest neighbour solution: {}.".format(altered_nn_solution))
            # print("Altered nearest neighbour solution length: {:.3f}.".format(
            #     altered_nn_solution_length))
            ANN_time = t1-t0
            # print(
            #     "Found tour by altered nearest neighbour in {:.3f} seconds.".format(t1-t0))
            # # plot_tour(altered_nn_solution)

            t0 = time.clock()
            genetic_algorithm_solution = solver.genetic_algorithm(
                population_size=100, elite_group_size=2, mutation_rate=0.05, generation_count=500)
            t1 = time.clock()
            genetic_algorithm_solution_length = solver.tour_length(
                genetic_algorithm_solution)
            # print("Genetic algorithm solution length: {:.3f}.".format(
            #     genetic_algorithm_solution_length))
            GA_time = t1-t0
            # print(
            #     "Found tour by genetic algorithm in {:.3f} seconds.".format(t1-t0))

            with open('tsp_times_{}.csv'.format(i), 'a', newline='') as csvfile:
                datawriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([10, BF_time, BNB_time, NN_time,
                                     RNN_time, ANN_time, GA_time])

            with open('tsp_distances_{}.csv'.format(i), 'a', newline='') as csvfile:
                datawriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([i, brute_force_solution_length, branch_and_bound_solution_length, nn_solution_length,
                                     repeated_nn_solution_length, altered_nn_solution_length, genetic_algorithm_solution_length])

            # solver.plot_genetic_algorithm(
            #     population_size=1000, elite_group_size=10, mutation_rate=0.05, generation_count=2500)

            # plot_4_tours(repeated_nn_solution, nn_solution,
            #              altered_nn_solution, genetic_algorithm_solution)
            # plt.show()


if (__name__ == "__main__"):
    main()
else:
    print(__name__)
