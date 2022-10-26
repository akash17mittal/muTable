import math


class ConcentricCircle:

    def __init__(self, center=(0, 0), radius=10, thickness=10):
        self.center = center
        self.radius1 = radius
        self.radius2 = radius + thickness
        self.thickness = thickness

    def is_point_inside(self, point):
        assert len(point) == 2
        distance_from_center = math.sqrt(
            math.pow(point[0] - self.center[0], 2) + math.pow(point[1] - self.center[1], 2))
        return (distance_from_center > self.radius1) and (distance_from_center < self.radius2)
