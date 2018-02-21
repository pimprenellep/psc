from climbermodel cimport _ClimberModel
from libcpp cimport bool

cdef extern from "native/controller.hpp":
    cppclass _Controller "Controller":
        _Controller(_ClimberModel * climber)
        bool tests()
