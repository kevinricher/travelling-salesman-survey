from Point import Point
import random
from TSP_Errors import PointGenerationError


class PointGrid:
    def __init__(self, max_coord, point_count):
        self.max_coord = max_coord
        self.point_count = point_count
        self.points = []
        self._generate_grid_points()

    def _contains_point(self, point):
        for grid_point in self.points:
            if grid_point.equal_to_point(point):
                return True
        return False

    def _add_point(self, point):
        self.points.append(point)

    def _generate_point(self):
        # Try 100 times to generate a new valid point.
        i = 0
        while(i < 100):
            point = Point(random.randint(0, self.max_coord),
                          random.randint(0, self.max_coord))
            if self._contains_point(point):
                i = i + 1
                continue
            else:
                # Return negative point (against convention)
                self._add_point(point)
                return
        # Error out and try again.
        raise PointGenerationError(
            "Failed to generate new point too many times.")

    def _generate_grid_points(self):
        for i in range(0, 100):
            self._generate_point()
