from climbermodel cimport _ClimberModel

cdef class ClimberModel:
    cdef _ClimberModel *thisobject
    def __cinit__(self, Morphology morphology):
        self.thisobject = new _ClimberModel(morphology.thisobject);

    def __dealloc__(self):
        del self.thisobject
