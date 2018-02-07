from .route             import Route
from .stancegraph       import StanceGraph
from .dummyexplorer     import DummyExplorer
from .dijkstraexplorer      import DijkstraExplorer

class Application :
    def cotationFromImage(self, image) :
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = DijkstraExplorer(stanceGraph)
        explorer.findPath()

    def testODE(self, image):
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = DummyExplorer(stanceGraph)
        explorer.findPath()
        if any([
            explorer.tests()
            ]):
            print("ODE tests failed")
            return True
        else:
            return False

    def testHighLevel(self, image):
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = DijkstraExplorer(stanceGraph)
        explorer.findPath()

        return False

    def tests(self, image) :
        if any([
            self.testODE(image),
            self.testHighLevel(image)
            ]):
            print("Global tests failed")
            return True
        else:
            return False


