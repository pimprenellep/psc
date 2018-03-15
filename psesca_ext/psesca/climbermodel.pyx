from psesca.morphology cimport Morphology

cdef class ClimberModel:
    def __cinit__(self, Morphology morphology):
        self.thisptr = new _ClimberModel(morphology.thisobject)

    def __dealloc__(self):
        del self.thisptr
