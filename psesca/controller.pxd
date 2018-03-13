from climbermodel cimport _ClimberModel
from stancegraph cimport _StanceGraph
from libcpp cimport bool

cdef extern from "native/controller.hpp":
    cppclass _Controller "Controller":
        _Controller(_ClimberModel * climber, _StanceGraph * stanceGraph)
        bool tests()

cdef class Controller:
    cdef _Controller * thisptr
