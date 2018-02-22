from shape cimport _Shape

cdef class Shape:
    cdef _Shape * thisptr
