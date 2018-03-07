from stancegraph cimport _StanceGraph
from route cimport _Route

cdef class StanceGraph :
    cdef _StanceGraph *thisptr
    cdef object pyroute
    def __cinit__(self, Route route) :
        self.thisptr = new _StanceGraph(route.thisptr)
        self.pyroute = route

    def __dealloc__(self):
        del self.thisptr

    def getRoute(self):
        return self.pyroute

    def getGraphRep(self):
        return ([], [])
        

