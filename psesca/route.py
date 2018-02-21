from abc import ABC,abstractmethod
from collections import namedtuple

Hold=namedtuple("Hold", ["x", "y", "shape"])

class Route(ABC) :
    def __init__(self, image):
        self.holds = []

    def getHolds(self):
        return self.holds
