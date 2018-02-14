from .stancegraph       import StanceGraph
from .factory           import Factory
from .defaultfactory    import DefaultFactory
from .jsonroutestore    import JSONRouteStore


class Application :
    def __init__(self):
        Factory.set(DefaultFactory())
        self.routeStore = JSONRouteStore('../samples/json_v1')

    def cotationFromImage(self, image) :
        route = self.routeStore.getRoute('verte')
        stanceGraph = StanceGraph(route)
        explorer = Factory.get().buildExplorer(stanceGraph)
        explorer.findPath()

    def tests(self, image):
        route = self.routeStore.getRoute('verte')
        stanceGraph = StanceGraph(route)
        explorer = Factory.get().buildExplorer(stanceGraph)
        if any([
            explorer.tests()
            ]):
            print("Global tests failed")
            return True
        else:
            return False
