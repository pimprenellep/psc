from .dijkstraexplorer import DijkstraExplorer
from .native import Controller
from .renderer import Renderer

class DefaultFactory:

    def buildExplorer(self, *args):
        return DijkstraExplorer(*args)
    def buildController(self, *args):
        return Controller(*args)
    def buildRenderer(self, *args):
        return Renderer(*args)
