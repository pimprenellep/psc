from .native import Controller


class DummyController(Controller):

    def __init__(self, climber, stanceGraph):
        #super().__init__(climber, stanceGraph)
        pass

    def tryStep(startPosition, startState, endPosition) :
        print("Dummy controller, tryStep not implemented.")

    def tests(self):
        print("Dummy controller, skipping tests")


