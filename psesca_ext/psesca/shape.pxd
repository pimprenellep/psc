cdef extern from "native/shape.hpp":
    cppclass _Shape "Shape":
        void glDraw(float x, float y)

cdef class Shape:
    cdef _Shape * thisptr
