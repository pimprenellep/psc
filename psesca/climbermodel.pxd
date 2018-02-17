from morphology cimport _Morphology

cdef extern from "native/climbermodel.hpp":
    cdef cppclass _ClimberModel "ClimberModel":
        _ClimberModel(_Morphology *m) except +

