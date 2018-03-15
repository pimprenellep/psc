from psesca.shape cimport _Shape, Shape

cdef extern from "native/wha_shape.hpp":
    cppclass _WHAShape "WHAShape":
        _WHAShape(float width, float height, float area)

cdef class WHAShape(Shape) :
    pass
