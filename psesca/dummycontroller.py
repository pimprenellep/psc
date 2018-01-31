from .controller import Controller
from .simulator import Simulator


class DummyController(Controller):

    def __init__(self, climber, stanceGraph):
        self.climber = climber
        self.graph = stanceGraph
        self.simulator = Simulator(stanceGraph.getRoute())
        self.simulator.addClimber(climber)

    def tryStep(startPosition, startState, endPosition) :
        print("Not implemented.")


