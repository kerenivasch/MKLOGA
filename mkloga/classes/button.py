from helpers import *
from classes.location import Location
from classes.size import Size

class Button:
    def __init__(self, id, location, size):
        self.id = id
        self.location = Location(x=location['x'], y=location['y'])
        self.size = Size(width=size['width'], height=size['height'])
        self.top_left = Location(x=self.location.x, y=self.location.y)
        self.top_right = Location(x=self.location.x + self.size.width, y=self.location.y)
        self.bottom_right = Location(x=self.location.x + self.size.width, y=self.location.y + self.size.height)
        self.bottom_left = Location(x=self.location.x, y=self.location.y + self.size.height)
        self.center = Location(x=self.location.x + self.size.width / 2, y=self.location.y + self.size.height / 2)
        self.text_origin = Location(x=self.location.x + 0.25, y=self.location.y + self.size.height - 0.35)

    def is_overlapping(self, other):
        if self.top_left.x > other.bottom_right.x or other.top_left.x > self.bottom_right.x:
            return False

        if self.top_left.y > other.bottom_right.y or other.top_left.y > self.bottom_right.y:
            return False

        return True
