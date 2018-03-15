from psesca.route cimport _Route

cdef extern from "native/stancegraph.hpp":
    cppclass _StanceGraph "StanceGraph":
        _StanceGraph(_Route *route)

cdef class StanceGraph :
    cdef _StanceGraph *thisptr
    cdef object pyroute
