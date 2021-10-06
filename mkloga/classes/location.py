import math
import numpy as np

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def euclidean_distance(self, other):
        xx = self.x - other.x
        yy = self.y - other.y
        return math.sqrt(xx * xx + yy * yy)
