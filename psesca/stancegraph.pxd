from route cimport _Route

cdef extern from "native/stancegraph.hpp":
    cppclass _StanceGraph "StanceGraph":
        _StanceGraph(const _Route *route)
