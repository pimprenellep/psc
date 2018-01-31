from abc import ABC,abstractmethod

class Controller:
    @abstractmethod
    def __init__(self, climber, stanceGraph):
        pass

    @abstractmethod
    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        if any([
            self.simulator.tests()
            ]):
            print("Controller tests failed")
            return True
        else:
            return False
