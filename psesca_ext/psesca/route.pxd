from psesca.shape cimport _Shape

cdef extern from "native/route.hpp":
    struct _Hold "Hold":
        float x
        float y
        _Shape *shape

    cppclass _Route "Route":
        _Route(int nHolds, _Hold *holds)

cdef class Route:
    cdef _Route *thisptr
