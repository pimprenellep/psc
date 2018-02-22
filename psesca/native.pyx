from morphology cimport _Morphology

cdef class Morphology :
    cdef _Morphology *thisobject;
    def __cinit__(self,height, weight):
        self.thisobject = new _Morphology(height, weight);

    def __dealloc__(self):
        del self.thisobject;
from climbermodel cimport _ClimberModel

cdef class ClimberModel:
    cdef _ClimberModel *thisptr
    def __cinit__(self, Morphology morphology):
        self.thisptr = new _ClimberModel(morphology.thisobject);

    def __dealloc__(self):
        del self.thisptr
from controller cimport _Controller

cdef class Controller:
    cdef _Controller * thisptr

    def __init__(self, ClimberModel climber, StanceGraph stanceGraph):
        self.thisptr = new _Controller(climber.thisptr, stanceGraph.thisptr)

    def __dealloc__(self):
        del self.thisptr

    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        return self.thisptr.tests()
from shape cimport _Shape

cdef class Shape:
    cdef _Shape * thisptr
from shape cimport _Shape
from wha_shape cimport _WHAShape

cdef class WHAShape(Shape) :
    def __cinit__(self, width, height, area):
        self.thisptr = <_Shape *>new _WHAShape(width, height, area)

    def __dealloc__(self):
        del self.thisptr
from collections import namedtuple

from route cimport _Hold, _Route
from shape cimport _Shape
from libc.stdlib cimport malloc

Hold=namedtuple("Hold", ["x", "y", "shape"])

cdef class Route:
    cdef _Route *thisptr
    ## Constructor meant to be called by subclasses
    # holds is a list of Hold named tuples, shape must
    #  be a wrapper of a native shape object or one of
    #  its subclasses
    def __init__(self, holds):
        cdef int n = len(holds)
        cdef _Hold * _holds = <_Hold *>malloc(n * sizeof(_Hold))
        cdef int i

        self.__holds = holds
        for i in range(n):
                _holds[i].x = holds[i].x
                _holds[i].y = holds[i].y
                _holds[i].shape = (<Shape>holds[i].shape).thisptr
        self.thisptr = new _Route(n, _holds)

    def __dealloc__(self):
        del self.thisptr
    
    def getHolds(self):
        return self.__holds
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
        

