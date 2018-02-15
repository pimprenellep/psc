from abc import ABC, abstractmethod

## Abstract shape of a hold
#
# Since the shape can be represented in many different ways,
# all that depends on the shape should be encapsulated in a subclass a this one.
class Shape(ABC):
    ## Draw the hold in current OpenGL context
    @abstractmethod
    def glDraw(self, x, y):
        pass
    
