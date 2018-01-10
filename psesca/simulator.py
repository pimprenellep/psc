from ode import World

class Simulator:
    def __init__(self, climber, route):
        self.world = World()
        climber.addToODE(self, 0, 0, 0)

    def getWorld(self):
        return self.world

