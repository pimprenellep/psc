from abc import ABC,abstractmethod
from .morphology import Morphology
from .climbermodel import ClimberModel
from .factory import Factory

class Explorer(ABC) :
    def __init__(self, stanceGraph):
        morphology = Morphology(1.70, 60)
        self.climber = ClimberModel(morphology)
        self.graph = stanceGraph
        self.controller = Factory.get().buildController(self.climber, stanceGraph)

    @abstractmethod
    def findPath(self):
        pass

    def tests(self) :
        if any([
            self.controller.tests()
            ]):
            print("Explorer tests failed")
            return True
        else:
            return False

