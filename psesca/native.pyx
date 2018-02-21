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

    def __init__(self, ClimberModel climber, stanceGraph):
        self.thisptr = new _Controller(climber.thisptr)

        #self.graph = stanceGraph

    def __dealloc__(self):
        del self.thisptr

    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        return self.thisptr.tests()
from wha_shape cimport _WHAShape

cdef class WHAShape :
    cdef _WHAShape * thisptr
    def __cinit__(self, width, height, area):
        self.thisptr = new _WHAShape(width, height, area)

    def __dealloc__(self):
        del self.thisptr
