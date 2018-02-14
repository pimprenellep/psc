from .routestore import RouteStore
from .jsonbasicroute import JSONBasicRoute

## Basic store loading routes from json files
#
# Those json files are meant to be used as cache files for route 
# generated from photographies, possibly involving user interaction
class JSONRouteStore(RouteStore):
    ## Constructor
    # @param jsondir Directory under which json files are stored
    def __init__(self, jsondir):
        self.dir = jsondir

    ## Retrieves a route from the store
    # @param routeId basename of the json file to load
    def getRoute(self, routeId):
        f = open(self.dir + '/' + routeId + ".json")
        jtext = f.read()
        return JSONBasicRoute(jtext)
