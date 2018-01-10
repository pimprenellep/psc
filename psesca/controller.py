from abc import ABC,abstractmethod

class Controller:
    #tryStep(startPosition:int,startState:MechState, endPosition:int): (bool, MechState, Difficulty)
    @abstractmethod
    def tryStep(startPosition, startState, endPosition):
        pass
