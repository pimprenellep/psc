from morphology cimport _Morphology

cdef class Morphology :
    cdef _Morphology *thisobject;
    def __cinit__(self,height, weight):
        self.thisobject = new _Morphology(height, weight);

    def __dealloc__(self):
        del self.thisobject;
