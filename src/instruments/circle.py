import math


class Circle:

    def __init__(self, center=(0, 0), radius=10):
        print("###########", center)
        self.center = center
        self.radius = radius

    def is_point_inside(self, point):
        assert len(point) == 2
        distance_from_center = math.sqrt(
            math.pow(point[0] - self.center[0], 2) + math.pow(point[1] - self.center[1], 2))
        return distance_from_center < self.radius
