from morphology cimport _Morphology

cdef class Morphology :
    cdef _Morphology *thisobject;
    def __cinit__(self,height, weight):
        self.thisobject = new _Morphology(height, weight);

    def __dealloc__(self):
        del self.thisobject;
from climbermodel cimport _ClimberModel

cdef class ClimberModel:
    cdef _ClimberModel *thisobject
    def __cinit__(self, Morphology morphology):
        self.thisobject = new _ClimberModel(morphology.thisobject);

    def __dealloc__(self):
        del self.thisobject
from abc import ABC,abstractmethod
from .factory import Factory

class Controller:
    def __init__(self, climber, stanceGraph):
        self.climber = climber
        self.graph = stanceGraph
        #self.simulator = Factory.get().buildSimulator(stanceGraph.getRoute())
        #self.simulator.addClimber(climber)

    @abstractmethod
    def tryStep(self, startPosition, startState, endPosition):
        pass

    def tests(self) :
        if any([
            False #self.simulator.tests()
            ]):
            print("Controller tests failed")
            return True
        else:
            return False
