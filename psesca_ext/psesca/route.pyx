from collections import namedtuple

from psesca.shape cimport Shape
from libc.stdlib cimport malloc

Hold=namedtuple("Hold", ["x", "y", "shape"])

cdef class Route:
    ## Constructor meant to be called by subclasses
    # holds is a list of Hold named tuples, shape must
    #  be a wrapper of a native shape object or one of
    #  its subclasses
    def __init__(self, holds):
        cdef int n = len(holds)
        cdef _Hold * _holds = <_Hold *>malloc(n * sizeof(_Hold))
        cdef int i

        self.__holds = holds
        for i in range(n):
                _holds[i].x = holds[i].x
                _holds[i].y = holds[i].y
                _holds[i].shape = (<Shape>holds[i].shape).thisptr
        self.thisptr = new _Route(n, _holds)

    def __dealloc__(self):
        del self.thisptr
    
    def getHolds(self):
        return self.__holds
