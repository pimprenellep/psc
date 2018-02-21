from controller cimport _Controller

cdef class Controller:
    cdef _Controller * thisptr

    def __init__(self, ClimberModel climber, stanceGraph):
        self.thisptr = new _Controller(climber.thisptr)

        #self.graph = stanceGraph

    def __dealloc__(self):
        del self.thisptr

    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        return self.thisptr.tests()
