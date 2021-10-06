import copy

from classes.location import Location

class Finger:
    def __init__(self, location):
        self.location = Location(x=location['x'], y=location['y'])
