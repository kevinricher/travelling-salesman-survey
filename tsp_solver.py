import itertools
from point import Point
from point_grid import PointGrid


class TSP_Solver:
    def __init__(self, max_coord=10, point_count=5, seed=41):
        self.max_coord = max_coord
        self.point_count = point_count
        self.seed = seed
        self.instance = PointGrid(max_coord=self.max_coord,
                                  point_count=self.point_count, seed=self.seed)
        print("Instance points: {}.".format(self.instance.points))

    @staticmethod
    def tour_length(tour):
        "The total of distances between each pair of consecutive cities in the tour."
        return sum(Point.distance(tour[i], tour[i-1])
                   for i in range(len(tour)))

    @staticmethod
    def first(collection):
        return next(iter(collection))

    # Brute force methods.
    def get_all_tours(self):
        start = self.first(self.instance.points)
        print("First vertex: {}.".format(start))
        return [[start] + list(rest) for rest in itertools.permutations(frozenset(self.instance.points) - {start})]

    def shortest_tour(self, tours):
        return min(tours, key=self.tour_length)

    def brute_force(self):
        "Check all tours."
        all_tours = self.get_all_tours()
        return self.shortest_tour(all_tours)

    # Nearest neighbour methods.
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

    # Segment reversal methods.
    def reverse_segment_if_better(self, tour, i, j):
        "If reversing tour[i:j] would make the tour shorter, then do it."
        # Given tour [...A-B...C-D...], consider reversing B...C to get
        # [...A-C...B-D...]
        p1, p2, p3, p4 = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
        # Are old edges (AB + CD) longer than new ones (AC + BD)? If so,
        # reverse segment.
        if (Point.distance(p1, p2) + Point.distance(p3, p4) >
                Point.distance(p1, p3) + Point.distance(p2, p4)):
            tour[i:j] = reversed(tour[i:j])

    def alter_tour(self, tour):
        "Try to alter tour for the better by reversing segments."
        original_length = self.tour_length(tour)
        for (start, end) in self.all_segments(len(tour)):
            self.reverse_segment_if_better(tour, start, end)
            # If we made an improvement, then try again; else stop and return tour.
            if self.tour_length(tour) < original_length:
                return self.alter_tour(tour)
            return tour

    def altered_nearest_neighbour(self):
        "Run nearest neighbor TSP algorithm, and alter the results by reversing segments."
        return self.alter_tour(self.nearest_neighbour())

    @staticmethod
    def all_segments(N):
        "Return (start, end) pairs of indexes that form segments of tour of length N."
        return [(start, start + length)
                for length in range(N, 2-1, -1)
                for start in range(N - length + 1)]

    # Repeated nearest neighbour methods.
    def repeated_nearest_neighbour():
        pass
