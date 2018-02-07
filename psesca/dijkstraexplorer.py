from .explorer import Explorer
from .morphology import Morphology
from .climbermodel import ClimberModel
from .dummycontroller import DummyController

class DijkstraExplorer(Explorer) :
    def __init__(self, stanceGraph):
        morphology = Morphology(170, 60)
        self.climber = ClimberModel(morphology)
        self.graph = stanceGraph
        self.controller = DummyController(self.climber, stanceGraph)

    def findPath(self):
        G, Lpos = self.graph.getGraphRep()
        Lprises = self.graph.getRoute().getHolds()

        # Code du parcours de graphe
        print("Traversing graph")

