from ode import World, Body, BallJoint

from .climbermodel import ClimberModel

from numpy import array, matrix, identity
from collections import namedtuple
from queue import Queue

class Simulator:
    def __init__(self, route):
        self.world = World()

        self.ODEParts = []
        self.ODEJoints = []

    def getWorld(self):
        return self.world

    def addClimber(self, model):
        self.model = model
        climber = model.getComponents()
        self.climber = climber
        
        
        for p in range(climber.nParts):
            b = Body(self.world)
            self.ODEParts.append(b)
            b.setRotation(climber.parts[p].refRot.flat)
        
        
        for j in range(climber.nJoints):
            if model.joints[j].freedom == ClimberModel.JointType.Hinge :
                self.ODEJoints.append(HingeJoint(self.world))
            else:
                self.ODEJoints.append(BallJoint(self.world))
            (p1, p2) = climber.joints[j].bodies
            self.ODEJoints[j].attach(self.ODEParts[p1], self.ODEParts[p2])
            
        closed = set()
        op = Queue()
        op.put(0)
        
        while(not op.empty()):
            p1 = op.get()
            b1 = self.ODEParts[p1]
            pos1 = array(b1.getPosition())
            rot1 = matrix(b1.getRotation())
            rot1.shape = (3,3)
        
            for j in climber.parts[p1].jointsId :
                j_p1 = 0 if climber.joints[j].bodies[0] == p1 else 1
                p2 = climber.joints[j].bodies[1 - j_p1]
                anchor = pos1 + rot1.dot( climber.parts[p1].bbox * climber.joints[j].relAnchors[j_p1] )
                anchor2 = climber.parts[p2].refRot.dot( climber.parts[p2].bbox * climber.joints[j].relAnchors[1 - j_p1] )
                self.ODEParts[p2].setPosition((anchor - anchor2).flat)
                self.ODEJoints[j].setAnchor(anchor.flat)
                
                if(not p2 in closed):
                    op.put(p2)
            closed.add(p1)
            
        self.dumpFromOde()

    def dumpFromOde(self):
        print("Positions of all parts :")
        for p in range(self.climber.nParts):
            print("\tPart " + str(p) + " (" + self.climber.parts[p].name + ") :" + str(self.ODEParts[p].getPosition()))
