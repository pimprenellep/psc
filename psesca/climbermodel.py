from abc import ABC,abstractmethod

from numpy import array, matrix, identity
from collections import namedtuple

ClimberPart = namedtuple('ClimberPart', ['name', 'bbox', 'mass', 'refRot', 'jointsId'])
ClimberJoint = namedtuple('ClimberJoint', ['bodies', 'relAnchors'])
ClimberComponents = namedtuple('ClimberComponents', ['parts', 'nParts', 'joints', 'nJoints'])

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
        
        for j in range(self.nJoints):
            for p in self.joints[j].bodies :
                self.parts[p].jointsId.append(j)

    def getComponents(self):
        return ClimberComponents(
                parts=self.parts, nParts=self.nParts,
                joints=self.joints, nJoints=self.nJoints
            )
