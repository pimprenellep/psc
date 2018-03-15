cdef class WHAShape:
    def __cinit__(self, width, height, area):
        self.thisptr = <_Shape *>new _WHAShape(width, height, area)

    def __dealloc__(self):
        del self.thisptr
