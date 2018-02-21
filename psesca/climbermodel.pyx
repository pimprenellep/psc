from climbermodel cimport _ClimberModel

cdef class ClimberModel:
    cdef _ClimberModel *thisptr
    def __cinit__(self, Morphology morphology):
        self.thisptr = new _ClimberModel(morphology.thisobject);

    def __dealloc__(self):
        del self.thisptr
