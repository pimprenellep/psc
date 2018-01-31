from abc import ABC,abstractmethod

from ode import Body, BallJoint

from numpy import array, matrix, identity
from collections import namedtuple
from queue import Queue

# FIXME : some propoerties should be externalized in a mechstate struct
# (All that can change with time)

ClimberPart = namedtuple('ClimberPart', ['name', 'bbox', 'mass', 'refRot', 'jointsId'])
ClimberJoint = namedtuple('ClimberJoint', ['bodies', 'relAnchors'])

class ClimberModel(ABC):
    
    def __init__(self, morphology):
        self.morphology = morphology
        self.parts = [
                ClimberPart(
                    name='lbody',
                    bbox=array((1.0,1.0,1.0)), 
                    mass=0,
                    refRot=identity(3), 
                    jointsId=[]
                ),
                ClimberPart(
                    name='ubody',
                    bbox=array((1.0,1.0,1.0)), 
                    mass=0,
                    refRot=identity(3), 
                    jointsId=[]
                )]
        self.nParts = len(self.parts)
        self.joints = [
                ClimberJoint(
                    bodies=(0,1),
                    relAnchors=(array((0.0, 0.0, 0.5)), array((0.0,0.0,-0.5)))
                )]
        self.nJoints = len(self.joints)
        self.ODEParts = []
        self.ODEJoints = []
        
        self.partsPos = [ None ] * self.nParts
        
        for j in range(self.nJoints):
            for p in self.joints[j].bodies :
                self.parts[p].jointsId.append(j)

    def addToODE(self, simulator, x0, y0, z0):
        world = simulator.getWorld()
        
        for p in range(self.nParts):
            b = Body(world)
            self.ODEParts.append(b)
            b.setRotation(self.parts[p].refRot.flat)
        
        
        for j in range(self.nJoints):
            # FIXME : joint type ???
            self.ODEJoints.append(BallJoint(world))
            (p1, p2) = self.joints[j].bodies
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
        
            for j in self.parts[p1].jointsId :
                j_p1 = 0 if self.joints[j].bodies[0] == p1 else 1
                p2 = self.joints[j].bodies[1 - j_p1]
                anchor = pos1 + rot1.dot( self.parts[p1].bbox * self.joints[j].relAnchors[j_p1] )
                anchor2 = self.parts[p2].refRot.dot( self.parts[p2].bbox * self.joints[j].relAnchors[1 - j_p1] )
                self.ODEParts[p2].setPosition((anchor - anchor2).flat)
                self.ODEJoints[j].setAnchor(anchor.flat)
                
                if(not p2 in closed):
                    op.put(p2)
            closed.add(p1)
            
        self.dumpFromOde()

    def dumpFromOde(self):
        print("Positions of all parts :")
        for p in range(self.nParts):
            print("\tPart " + str(p) + " (" + self.parts[p].name + ") :" + str(self.ODEParts[p].getPosition()))
