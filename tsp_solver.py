import itertools
import tsp_plot
from point import Point
from point_grid import PointGrid


class TSP_Solver:
    def __init__(self, max_coord=10, point_count=5, seed=41):
        self.max_coord = max_coord
        self.point_count = point_count
        self.seed = seed
        self.instance = PointGrid(
            max_coord=self.max_coord, point_count=self.point_count, seed=self.seed)

    @staticmethod
    def tour_length(tour):
        "The total of distances between each pair of consecutive cities in the tour."
        return sum(Point.distance(tour[i], tour[i-1])
                   for i in range(len(tour)))

    @staticmethod
    def first(collection):
        return next(iter(collection))

    def get_all_tours(self):
        start = self.first(self.instance.points)
        print(type(self.instance.points))
        return [[start] + list(rest) for rest in itertools.permutations({self.instance.points} - {start})]

    def brute_force(self):
        "Check all tours."
        all_tours = itertools.permutations(self.instance.points)
        return min(all_tours, key=self.tour_length)

    @staticmethod
    def _find_nearest_neighbour(key_point, points):
        return min(points, key=lambda c: Point.distance(c, key_point))

    def nearest_neighbour(self):
        "Append each nearest city to form a tour."
        start = self.first(self.instance.points)
        tour = [start]
        unvisited = (frozenset(self.instance.points) - {start})
        while unvisited:
            C = self._find_nearest_neighbour(tour[-1], unvisited)
            tour.append(C)
            unvisited.remove(C)
        return tour
