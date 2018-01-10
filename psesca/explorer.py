from abc import ABC,abstractmethod

class Explorer(ABC) :
    def __init__(self, route):
        pass
    @abstractmethod
    def findPath(self):
        pass

