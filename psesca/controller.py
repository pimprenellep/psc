from abc import ABC,abstractmethod

class Controller:
    @abstractmethod
    def __init__(self, climber, stanceGraph):
        pass

    @abstractmethod
    def tryStep(self, startPosition, startState, endPosition):
        pass
