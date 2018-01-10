from abc import ABC,abstractmethod

class Explorer(ABC) :
    @abstractmethod
    def __init__(self, stanceGraph):
        pass
    @abstractmethod
    def findPath(self):
        pass

