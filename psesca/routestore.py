from abc import ABC,abstractmethod

## Abstract store for the routes
#
# This class is an interface allowing the core components to retrieve data for a route without
# caring about how route are stored.

class RouteStore(ABC):
    ## Retrieves a route from the store
    # @param routeId abstract identifier for a route in the store
    @abstractmethod
    def getRoute(self, routeId):
        pass:

