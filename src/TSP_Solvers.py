import itertools
import TSP_Plot
from Point import Point
from PointGrid import PointGrid


class TSP_Solver:
    def __init__(self, max_coord=10, point_count=5, seed=41):
        self.max_coord = max_coord
        self.point_count = point_count
        self.seed = seed
        self.instance = PointGrid(
            max_coord=self.max_coord, point_count=self.point_count, seed=self.seed)

    def tour_length(self, tour):
        "The total of distances between each pair of consecutive cities in the tour."
        return sum(Point.distance(tour[i], tour[i-1])
                   for i in range(len(tour)))

    def brute_force(self):
        "Check all tours."
        all_tours = itertools.permutations(self.instance.points)
        return min(all_tours, key=self.tour_length)
