from psesca.route cimport Route

cdef class StanceGraph :
    def __cinit__(self, Route route) :
        self.thisptr = new _StanceGraph(route.thisptr)
        self.pyroute = route

    def __dealloc__(self):
        del self.thisptr

    def getRoute(self):
        return self.pyroute

    def getGraphRep(self):
        return ([], [])
        

