from controller cimport _Controller
from climbermodel cimport ClimberModel
from stancegraph cimport StanceGraph

cdef class Controller:
    def __init__(self, ClimberModel climber, StanceGraph stanceGraph):
        self.thisptr = new _Controller(climber.thisptr, stanceGraph.thisptr)

    def __dealloc__(self):
        del self.thisptr

    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        return self.thisptr.tests()
