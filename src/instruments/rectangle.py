import math


class Rectangle:

    def __init__(self, topLeft=(0, 0), bottomRight=(0, 0)):
        self.topLeft = topLeft
        self.bottomRight = bottomRight

    def is_point_inside(self, point):
        assert len(point) == 2
        return (point[0] > self.topLeft[0]) and (point[0] < self.bottomRight[0]) and (point[1] > self.topLeft[1]) and (point[1] < self.bottomRight[1])