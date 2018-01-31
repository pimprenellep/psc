from abc import ABC,abstractmethod

class Explorer(ABC) :
    @abstractmethod
    def __init__(self, stanceGraph):
        pass
    @abstractmethod
    def findPath(self):
        pass

    def tests(self) :
        if any([
            self.controller.tests()
            ]):
            print("Explorer tests failed")
            return True
        else:
            return False

