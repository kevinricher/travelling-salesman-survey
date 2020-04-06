from point import Point
import math


class LineSegment:
    def __init__(self, start_point, end_point):
        self.p1 = start_point
        self.p2 = end_point
        self.length = Point.distance(self.p1, self.p2)
        self.direction = self._calculate_direction()

    def _calculate_direction(self):
        return Point((self.p2 - self.p1).real / self.length, (self.p2 - self.p1).imag / self.length)

    def parallel_to_segment(self, segment):
        if ((math.isclose(self.direction.x, segment.direction.x, rel_tol=1e-5) and
             (math.isclose(self.direction.y, segment.direction.y, rel_tol=1e-5)))):
            return True
        else:
            return False

    def contains_point(self, point):
        point_distance = Point.distance(
            self.p1, point) + Point.distance(self.p2, point)
        return math.isclose(self.length, point_distance, rel_tol=1e-5)

    def overlaps_with_segment(self, segment):
        if not self.parallel_to_segment(segment):
            return False
        if self.contains_point(segment.p1) or self.contains_point(segment.p2):
            return True
        else:
            return False
