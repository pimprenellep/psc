# distutils: language=c++

from psesca.climbermodel cimport ClimberModel
from psesca.stancegraph cimport StanceGraph, _Stance

cdef class MechState:
    cdef _MechState * thisptr
    def __cinit__(self):
        self.thisptr = NULL
    cdef setState(self, _MechState * state):
        self.thisptr = state

## Python wrapper for the controller
cdef class Controller:
    ## Initialize the underlying engines with route and climber
    def __init__(self, ClimberModel climber, StanceGraph stanceGraph):
        self.__thisptr = new _Controller(climber.thisptr, stanceGraph.thisptr)

    def __dealloc__(self):
        del self.__thisptr

    ## Main interface method : try to make a move
    def tryStep(self, startPosition, startState, endPosition):
        cdef _Stance s
        s.lf = startPosition.lf
        s.rf = startPosition.rf
        s.lh = startPosition.lh
        s.rh = startPosition.rh
        cdef _Stance e
        e.lf = endPosition.lf
        e.rf = endPosition.rf
        e.lh = endPosition.lh
        e.rh = endPosition.rh
        ##self.__thisptr.tryStep(s, startPosition.thisptr, e)

    def tests(self) :
        return self.__thisptr.tests()
