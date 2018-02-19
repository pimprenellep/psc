from wha_shape cimport _WHAShape

cdef class WHAShape :
    cdef _WHAShape * thisptr
    def __cinit__(self, width, height, area):
        self.thisptr = new _WHAShape(width, height, area)

    def __dealloc__(self):
        del self.thisptr
