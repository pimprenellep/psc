from .dijkstraexplorer import DijkstraExplorer
from .controller import Controller
from .simulator import Simulator

class DefaultFactory:

    def buildExplorer(self, *args):
        return DijkstraExplorer(*args)
    def buildController(self, *args):
        return Controller(*args)
    def buildSimulator(self, *args):
        return Simulator(*args)
