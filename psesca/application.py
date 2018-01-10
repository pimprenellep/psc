from .route             import Route
from .stancegraph       import StanceGraph
from .dummyexplorer     import DummyExplorer

class Application :
    def cotationFromImage(self, image) :
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = DummyExplorer(stanceGraph)
        explorer.findPath()

