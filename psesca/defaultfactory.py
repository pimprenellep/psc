from .dijkstraexplorer import DijkstraExplorer
from .controller import Controller

class DefaultFactory:

    def buildExplorer(self, *args):
        return DijkstraExplorer(*args)
    def buildController(self, *args):
        return Controller(*args)
