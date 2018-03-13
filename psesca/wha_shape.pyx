from shape cimport _Shape, Shape
from wha_shape cimport _WHAShape

cdef class WHAShape(Shape) :
    def __cinit__(self, width, height, area):
        self.thisptr = <_Shape *>new _WHAShape(width, height, area)

    def __dealloc__(self):
        del self.thisptr
