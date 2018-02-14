from abc import ABC,abstractmethod
from .factory import Factory

class Controller:
    def __init__(self, climber, stanceGraph):
        self.climber = climber
        self.graph = stanceGraph
        self.simulator = Factory.get().buildSimulator(stanceGraph.getRoute())
        self.simulator.addClimber(climber)

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
