cdef extern from "native/morphology.hpp":
    cdef cppclass _Morphology "Morphology":
        _Morphology(float h, float w) except +

cdef class Morphology :
    cdef _Morphology *thisobject;
    
