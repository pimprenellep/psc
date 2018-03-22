from psesca.route cimport _Route

cdef extern from "native/stancegraph.hpp":
    cppclass _StanceGraph "StanceGraph":
        _StanceGraph(_Route *route)
    ctypedef struct _Stance "Stance":
        int lf
        int rf
        int lh
        int rh

cdef class StanceGraph :
    cdef _StanceGraph *thisptr
    cdef object pyroute
