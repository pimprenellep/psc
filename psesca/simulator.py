#from ode import World, Body, BallJoint, Mass, AMotor, AMotorEuler
from ode import *
import scipy.constants

from .climbermodel import ClimberModel

from numpy import array, matrix, identity
from collections import namedtuple
from queue import Queue

class Simulator:
    def __init__(self, route):
        self.world = World()
        self.world.setGravity((0.0, 0.0, -scipy.constants.g))

        self.ODEParts = []
        self.ODEJoints = []
        self.ODEMotors = []

    def getWorld(self):
        return self.world

    def addClimber(self, model):
        self.model = model
        climber = model.getComponents()
        self.climber = climber
        
        
        for p in range(climber.nParts):
            cp = climber.parts[p]
            b = Body(self.world)
            self.ODEParts.append(b)
            b.setRotation(cp.refRot.flat)
            m = Mass()
            if cp.shape == ClimberModel.PartShape.Cylinder :
                m.setCylinderTotal(cp.mass, 3, min(cp.bbox[0], cp.bbox[1])/2.0, cp.bbox[2])
            else :
                raise NotImplementedError("Unknown segment shape requested : {}".format(cp.shape))
            b.setMass(m)
        
        
        for j in range(climber.nJoints):
            if climber.joints[j].freedom == ClimberModel.JointType.Hinge :
                self.ODEJoints.append(HingeJoint(self.world))
            elif climber.joints[j].freedom == ClimberModel.JointType.Ball :
                self.ODEJoints.append(BallJoint(self.world))
            else :
                raise NotImplementedError("Unknown joint type requested : {}".format(climber.joints[j].freedom))
            self.ODEMotors.append(AMotor(self.world))
            (p1, p2) = climber.joints[j].bodies
            self.ODEJoints[j].attach(self.ODEParts[p1], self.ODEParts[p2])
            self.ODEMotors[j].attach(self.ODEParts[p1], self.ODEParts[p2])
            
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

                rot2 = climber.parts[p2].refRot
                anchor = pos1 + rot1.dot( climber.parts[p1].bbox * climber.joints[j].relAnchors[j_p1] )
                anchor2 = rot2.dot( climber.parts[p2].bbox * climber.joints[j].relAnchors[1 - j_p1] )
                self.ODEParts[p2].setPosition((anchor - anchor2).flat)
                self.ODEJoints[j].setAnchor(anchor.flat)
                
                m = self.ODEMotors[j]
                m.setMode(AMotorEuler)
                m.setAxis(0, 1, rot1.dot(climber.joints[j].relAxes[0]).flat)
                m.setAxis(2, 2, rot2.dot(climber.joints[j].relAxes[1]).flat)
                for (param, value) in zip(
                        [ParamLoStop, ParamHiStop, ParamLoStop2, ParamHiStop2, ParamLoStop3, ParamHiStop3],
                        climber.joints[j].stops ):
                    m.setParam(param, value)

                if(not p2 in closed):
                    op.put(p2)
            closed.add(p1)
            
        self.dumpFromOde()

    def dumpFromOde(self):
        print("Positions of all parts :")
        for p in range(self.climber.nParts):
            print("\tPart " + str(p) + " (" + self.climber.parts[p].name + ") :" + str(self.ODEParts[p].getPosition()))

    def tests(self) :
        if any([
            self.testFreeFall(100.0, 100000, 1e-6)
            ]):
            print("Simulator tests failed")
            return True
        else:
            return False



    def testFreeFall(self, time, divs, tolerance):
        print("Test : free fall, time={}, divs={}, tolerance={}".format(time, divs, tolerance))

        ref = 0;
        pos0 = array(self.ODEParts[ref].getPosition())
        for i in range(divs):
            self.world.step(time / divs)
        pos = array(self.ODEParts[ref].getPosition())
        theo = array((0.0, 0.0, - scipy.constants.g * time * time / 2.0) )
        gap = (pos - pos0) - theo

        err2 = gap.dot(gap) / theo.dot(theo)

        if err2 > tolerance :
            print("Test free fall failed. (err2 = {}, tolerance = {})".format(err2, tolerance))
            return True

        print("Test free fall passed. (err2 = {}, tolerance = {})".format(err2, tolerance))
        return False


