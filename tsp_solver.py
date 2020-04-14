import itertools
import random
import operator
import math
import numpy as np
from point import Point
from point_grid import PointGrid
from matplotlib import pyplot as plt


class TSP_Solver:
    def __init__(self, max_coord=10, point_count=5, seed=41):
        self.max_coord = max_coord
        self.point_count = point_count
        self.seed = seed
        self.instance = PointGrid(max_coord=self.max_coord,
                                  point_count=self.point_count, seed=self.seed)

        self.bnb_tour = [None] * (point_count+1)
        self.bnb_final_res = float('inf')
        self.bnb_visited = [False] * point_count
        # print("Instance points: {}.".format(self.instance.points))

    @staticmethod
    def tour_length(tour):
        "The total of distances between each pair of consecutive cities in the tour."
        return sum(Point.distance(tour[i], tour[i-1])
                   for i in range(len(tour)))

    @staticmethod
    def first(collection):
        return next(iter(collection))

    # -- Brute force methods -- #

    def get_all_tours(self):
        start = self.first(self.instance.points)
        # print("First vertex: {}.".format(start))
        return [[start] + list(rest) for rest in itertools.permutations(frozenset(self.instance.points) - {start})]

    def shortest_tour(self, tours):
        return min(tours, key=self.tour_length)

    def brute_force(self):
        "Check all tours."
        all_tours = self.get_all_tours()
        return self.shortest_tour(all_tours)

    # -- Nearest neighbour methods -- #

    @staticmethod
    def _find_nearest_neighbour(key_point, points):
        return min(points, key=lambda c: Point.distance(c, key_point))

    def nearest_neighbour(self, start=None):
        "Append each nearest city to form a tour."
        if start is None:
            start = self.first(self.instance.points)
        tour = [start]
        unvisited = set(frozenset(self.instance.points) - {start})
        while unvisited:
            C = self._find_nearest_neighbour(tour[-1], unvisited)
            tour.append(C)
            unvisited.remove(C)
        return tour

    # -- Repeated nearest neighbour methods -- #

    def sample_points(self, sample_count, seed=41):
        random.seed(len(self.instance.points) * sample_count * seed)
        return random.sample(self.instance.points, sample_count)

    def repeated_nearest_neighbour(self, repititions=500):
        "Use different start points, return shortest."
        if repititions > len(self.instance.points):
            repititions = len(self.instance.points)
        return self.shortest_tour(self.nearest_neighbour(start)
                                  for start in self.sample_points(round(repititions)))

    # -- Segment reversal methods -- #

    def reverse_segment_if_better(self, tour, i, j):
        "If reversing tour[i:j] would make the tour shorter, then do it."
        # Given tour [...A-B...C-D...], consider reversing B...C to get
        # [...A-C...B-D...]
        p1, p2, p3, p4 = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
        # Are old edges (AB + CD) longer than new ones (AC + BD)? If so,
        # reverse segment.
        d1 = Point.distance(p1, p2) + Point.distance(p3, p4)
        d2 = Point.distance(p1, p3) + Point.distance(p2, p4)
        if (d1 > d2):
            tour[i:j] = reversed(tour[i:j])

    def alter_tour(self, tour):
        "Try to alter tour for the better by reversing segments."
        original_length = self.tour_length(tour)
        all_segments = self.all_segments(len(tour))
        for (start, end) in all_segments:
            self.reverse_segment_if_better(tour, start, end)
        # If we made an improvement, then try again; else stop and return tour.
        if (self.tour_length(tour) < original_length):
            return self.alter_tour(tour)
        return tour

    @staticmethod
    def all_segments(N):
        "Return (start, end) pairs of indexes that form segments of tour of length N."
        segments = []
        for length in range(N, 1, -1):
            for start in range(N - length + 1):
                segments.append((start, start+length))
        return segments

    def altered_nearest_neighbour(self):
        "Run nearest neighbor TSP algorithm, and alter the results by reversing segments."
        nearest_neighbour_solution = self.nearest_neighbour()
        self.altered_nn_base_length = self.tour_length(
            nearest_neighbour_solution)
        return self.alter_tour(nearest_neighbour_solution)

    # -- Branch and bound methods -- #

    def set_final_tour(self, tour_list):
        # Add first point to end.
        N = len(self.instance.points)
        final_tour = [None] * (N+1)
        final_tour[:N + 1] = tour_list[:]
        final_tour[N] = tour_list[0]
        self.bnb_tour = [self.instance.points[i] for i in final_tour]

    # Finds the distance between all nodes, defines edge weights.
    def get_distance_matrix(self):
        points = np.array(self.instance.points)
        m, n = np.meshgrid(points, points)
        return abs(m - n).tolist()

    # Finds minimum weighted edge connected to i
    def firstMin(self, distance_matrix, i):
        min = float('inf')
        N = len(distance_matrix)
        for k in range(N):
            if distance_matrix[i][k] < min and i != k:
                min = distance_matrix[i][k]

        return min

    # Finds second minimum weighted edge connected to i
    def secondMin(self, distance_matrix, i):
        first, second = float('inf'), float('inf')
        N = len(distance_matrix)
        for j in range(N):
            if i == j:
                continue
            if distance_matrix[i][j] <= first:
                second = first
                first = distance_matrix[i][j]
            elif(distance_matrix[i][j] <= second and
                 distance_matrix[i][j] != first):
                second = distance_matrix[i][j]
        return second

    def bnb_recursion(self, distance_matrix, current_bound, current_weight,
                      level, current_path):
        N = len(distance_matrix)
        # Recursion base case, all nodes covered.
        if level == N:
            # Check for edge connecting first and last points.
            if distance_matrix[current_path[level - 1]][current_path[0]] != 0:
                # Update weight of current path.
                curr_res = current_weight + \
                    distance_matrix[current_path[level - 1]][current_path[0]]
                if curr_res < self.bnb_final_res:
                    self.set_final_tour(current_path)
                    self.bnb_final_res = curr_res
            return

        # Build the tree.
        for i in range(N):
            # New points only.
            if (distance_matrix[current_path[level-1]][i] != 0 and
                    self.bnb_visited[i] is False):
                temp = current_bound
                current_weight += distance_matrix[current_path[level - 1]][i]

                # Calculate bound for level.
                if level == 1:
                    current_bound -= ((self.firstMin(distance_matrix, current_path[level - 1]) +
                                       self.firstMin(distance_matrix, i)) / 2)
                else:
                    current_bound -= ((self.secondMin(distance_matrix, current_path[level - 1]) +
                                       self.firstMin(distance_matrix, i)) / 2)

                # current_bound + current_weight is the actual lower bound
                # for the node that we have arrived on.
                # If current lower bound < final_res,
                # we need to explore the node further
                if current_bound + current_weight < self.bnb_final_res:
                    current_path[level] = i
                    self.bnb_visited[i] = True

                    # call TSPRec for the next level
                    self.bnb_recursion(distance_matrix, current_bound, current_weight,
                                       level + 1, current_path)

                # Else we have to prune the node by resetting
                # all changes to current_weight and current_bound
                current_weight -= distance_matrix[current_path[level - 1]][i]
                current_bound = temp

                # Reset visited vertices
                self.bnb_visited = [False] * len(self.bnb_visited)
                for j in range(level):
                    if current_path[j] != -1:
                        self.bnb_visited[current_path[j]] = True

    # Find tour by basic branch and bound algorithm.
    def branch_and_bound(self):
        # Re-initialize
        self.bnb_tour = [None] * (self.point_count+1)
        self.bnb_final_res = float('inf')
        self.bnb_visited = [False] * self.point_count

        # Calculate distance/ adjacency matrix.
        distance_matrix = self.get_distance_matrix()
        N = len(distance_matrix)

        # Calculate initial bound.
        current_bound = 0
        current_path = [-1] * (N+1)
        self.bnb_visited = [False] * N
        for i in range(N):
            current_bound += (self.firstMin(distance_matrix, i) +
                              self.secondMin(distance_matrix, i))

        current_bound = math.ceil(current_bound / 2)

        self.bnb_visited[0] = True
        current_path[0] = 0

        self.bnb_recursion(distance_matrix, current_bound,
                           0, 1, current_path)
        return self.bnb_tour

    # -- Genetic algorithm methods -- #
    def evaluate_individual_fitness(self, individual):
        return 1/self.tour_length(individual)

    def create_individual(self):
        # Randomly scramble the point list.
        return random.sample(self.instance.points, len(self.instance.points))

    def initalize_population(self, population_size):
        # Create a population of size 'population_size'
        population = []
        for i in range(0, population_size):
            population.append(self.create_individual())
        return population

    def evaluate_population_fitness(self, population):
        # Return a population sorted based on fitness from high to low.
        population_fitness = {}
        for i in range(0, len(population)):
            population_fitness[i] = self.evaluate_individual_fitness(
                population[i])
        return sorted(population_fitness.items(), key=operator.itemgetter(1), reverse=True)

    def get_parent_indices(self, sorted_population, elite_group_size):
        # Automatically take 'elite_group_size' individuals off the top.
        # Ensures preservation of high performers.
        parent_indices = []
        cumulative_fitness_sum = np.cumsum(sorted_population[:][1])
        cumulative_fitness_percentage = 100 * \
            cumulative_fitness_sum/sum(sorted_population[:][1])
        for i in range(0, elite_group_size):
            parent_indices.append(sorted_population[i][0])
        for i in range(0, len(sorted_population) - elite_group_size):
            # Generate random percentage (0-100%):
            pick_threshold = 100*random.random()
            for j in range(0, len(sorted_population)):
                # Pick individual, prioritizing higher ranking ones.
                if pick_threshold < cumulative_fitness_percentage[j]:
                    parent_indices.append(sorted_population[j][0])
                    break
        return parent_indices

    def get_mating_pool(self, population, parent_indices):
        # Use parent indices to select actual parents.
        mating_pool = [population[i] for i in parent_indices]
        return mating_pool

    def ordered_crossover(self, list1, list2, start_index, end_index):
        result_list = [None]*len(list1)
        next_add_index = end_index
        # Direct transfer
        for i in range(start_index, end_index):
            result_list[i] = list1[i]

        list2_iter = itertools.chain(list2[end_index:], list2[:end_index])
        for i in range(len(list2)):
            temp_gene = next(list2_iter)
            if temp_gene not in result_list:
                result_list[next_add_index] = temp_gene
                next_add_index = (next_add_index+1) % len(list1)

        return result_list

    def breed(self, parent1, parent2):
        # Randomly select a block of genes from parent1, transplant
        # into child, and then fill with parent2.
        child = [None]*len(parent1)

        # Get gene block to take from parent 1.
        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent1))

        start_gene_index = min(gene_a, gene_b)
        end_gene_index = max(gene_a, gene_b)

        child = self.ordered_crossover(
            parent1, parent2, start_gene_index, end_gene_index)
        return child

    def breed_population(self, mating_pool, elite_group_size):
        children = []
        pool = random.sample(mating_pool, len(mating_pool))

        # Retain 'elite_group_size' best individuals.
        for i in range(0, elite_group_size):
            children.append(mating_pool[i])

        # Randomly breed parents, add offspring to children.
        for i in range(0, len(mating_pool)-elite_group_size):
            child = self.breed(pool[i], pool[len(mating_pool)-i-1])
            children.append(child)
        return children

    def mutate_individual(self, individual, mutation_rate):
        # Swap mutate with specified probability.
        # 0 <= mutation_rate <= 1
        for gene1_index in range(len(individual)):
            if(random.random() < mutation_rate):
                gene2_index = int(random.random()*len(individual))

                gene1 = individual[gene1_index]
                gene2 = individual[gene2_index]

                individual[gene1_index] = gene2
                individual[gene2_index] = gene1
        return individual

    def mutate_population(self, population, mutation_rate):
        mutated_population = []
        # Give every individual in population a chance to mutate.
        for individual_index in range(0, len(population)):
            mutated_individual = self.mutate_individual(
                population[individual_index], mutation_rate)
            mutated_population.append(mutated_individual)
        return mutated_population

    def get_next_generation(self, current_generation, elite_group_size, mutation_rate):
        sorted_population = self.evaluate_population_fitness(
            current_generation)
        parent_indices = self.get_parent_indices(
            sorted_population, elite_group_size)
        mating_pool = self.get_mating_pool(current_generation, parent_indices)
        children = self.breed_population(mating_pool, elite_group_size)
        next_generation = self.mutate_population(children, mutation_rate)
        return next_generation

    # Produce a tour using a genetic algorithm
    def genetic_algorithm(self, population_size, elite_group_size, mutation_rate, generation_count):
        population = self.initalize_population(population_size)
        # print("Initial distance: {}.".format(
        #     1 / self.evaluate_population_fitness(population)[0][1]))
        for i in range(0, generation_count):
            population = self.get_next_generation(
                population, elite_group_size, mutation_rate)

        # print("Final distance: {}.".format(
        #     1 / self.evaluate_population_fitness(population)[0][1]))
        best_tour_index = self.evaluate_population_fitness(population)[0][0]
        best_tour = population[best_tour_index]
        return best_tour

    def plot_genetic_algorithm(self, population_size, elite_group_size, mutation_rate, generation_count):
        population = self.initalize_population(population_size)
        progress = []
        progress.append(1/self.evaluate_population_fitness(population)[0][1])

        # print("Initial distance: {}.".format(
        #     1 / self.evaluate_population_fitness(population)[0][1]))
        for i in range(0, generation_count):
            population = self.get_next_generation(
                population, elite_group_size, mutation_rate)
            progress.append(
                1/self.evaluate_population_fitness(population)[0][1])

        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
