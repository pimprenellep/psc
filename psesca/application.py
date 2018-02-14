from .route             import Route
from .stancegraph       import StanceGraph
from .factory           import Factory
from .defaultfactory    import DefaultFactory


class Application :
    def __init__(self):
        Factory.set(DefaultFactory())

    def cotationFromImage(self, image) :
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = Factory.get().buildExplorer(stanceGraph)
        explorer.findPath()

    def tests(self, image):
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = Factory.get().buildExplorer(stanceGraph)
        if any([
            explorer.tests()
            ]):
            print("Global tests failed")
            return True
        else:
            return False
