from psesca.route cimport Route

cdef class StanceGraph :
    def __cinit__(self):
        self.thisptr = NULL

    def __init__(self, Route route) :
        if not self.thisptr :
            self.thisptr = new _StanceGraph(route.thisptr)
            self.pyroute = route

    def __dealloc__(self):
        del self.thisptr

    def getRoute(self):
        return self.pyroute

    def getGraphRep(self):
        return ([], [])
        

