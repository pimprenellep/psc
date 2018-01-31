from abc import ABC,abstractmethod

class ClimberModel(ABC):
    
    def __init__(self, morphology):
        self.morphology = morphology

    @abstractmethod
    def addToODE(self, simulator, x0, y0, z0):
        pass;
        
