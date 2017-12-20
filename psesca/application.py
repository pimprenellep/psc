from .route         import Route
from .stancegraph   import StanceGraph
from .explorer      import Explorer

class Application :
    def cotationFromImage(self, image) :
        route = Route(image)
        stanceGraph = StanceGraph(route)
        explorer = Explorer(stanceGraph)
        explorer.findPath()

