from .explorer import Explorer
from .dummycontroller import DummyController
from .graphDij import *

class DijkstraExplorer(Explorer) :
    def __init__(self, stanceGraph):
        super().__init__(stanceGraph)

    def findPath(self):
        G, Lpos = self.graph.getGraphRep()
        Lprises = self.graph.getRoute().getHolds()

        # Code du parcours de graphe
        print("Traversing graph")
        #utilise Lprise et ini
    """create_Graph(1)
#ini et final à déterminer
print(shortest_path(graph,ini, final))
"""
