from .explorer import Explorer
from .morphology import Morphology
from .climbermodel import ClimberModel
from .dummycontroller import DummyController

# Does nothing but instantiating a controller
class DummyExplorer(Explorer) :
    def __init__(self, stanceGraph):
        morphology = Morphology(170, 60)
        self.climber = ClimberModel(morphology)
        self.graph = stanceGraph
        self.controller = DummyController(self.climber, stanceGraph)

    def findPath(self):
        print("Not implemented")
    
