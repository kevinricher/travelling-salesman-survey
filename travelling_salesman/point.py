import math


class Point(complex):
    # Subclass complex for addition, subtraction, magnitude functionality.
    x = property(lambda p: p.real)
    y = property(lambda p: p.imag)

    @staticmethod
    def distance(A, B):
        return abs(B-A)

    def _distance_to_point(self, point):
        return math.sqrt((point.y-self.y)**2+(point.x-self.x)**2)

    def equal_to_point(self, point):
        return math.isclose(self._distance_to_point(point), 0, rel_tol=1e-5)
