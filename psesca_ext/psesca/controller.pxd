# distutils: language=c++

from psesca.climbermodel cimport _ClimberModel
from psesca.stancegraph cimport _StanceGraph, _Stance
from libcpp cimport bool

cdef extern from "native/simulator.hpp":
    ctypedef struct _MechState "MechState":
        pass

cdef extern from "native/controller.hpp":
    cppclass _Controller "Controller":
        _Controller(_ClimberModel * climber, _StanceGraph * stanceGraph)
        void tryStep(_Stance startStance, _MechState startState, _Stance endStance)
        bool tests()

cdef class Controller:
    cdef _Controller * __thisptr
