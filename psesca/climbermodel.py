from abc import ABC,abstractmethod

from numpy import array, matrix, identity
from math import pi
from collections import namedtuple

ClimberPart = namedtuple('ClimberPart', ['name', 'bbox', 'mass', 'refRot', 'shape', 'jointsId'])
ClimberJoint = namedtuple('ClimberJoint', ['freedom', 'bodies', 'relAnchors', 'relAxes', 'stops'])
ClimberComponents = namedtuple('ClimberComponents', ['parts', 'nParts', 'joints', 'nJoints'])


class ClimberModel(ABC):
    class JointType:
        Hinge = 0
        Ball = 1
    class PartShape:
        Cylinder = 0
    
    def __init__(self, morphology):
        self.morphology = morphology
        m = self.morphology
        self.parts = [
                ClimberPart(
                    name='lbody',
                    bbox=array((1.0, 1.0, 1.0))*m.getLength('lbody'), 
                    mass=m.getWeight('lbody'),
                    refRot=identity(3), 
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='ubody',
                    bbox=array((1.0, 1.0, 1.0)) * m.getLength('ubody'), 
                    mass= m.getWeight('ubody'),
                    refRot=identity(3), 
                    #refRot=matrix([[0.0,-1.0,0.0],[1.0,0.0,0.0],[0.0,0.0,1.0]]),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='head',
                    bbox=array((1.0,1.0,1.0))* m.getLength('head'),
                    mass = m.getWeight('head'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ), 
                ClimberPart(
                    name='arm_right',
                    bbox=array((0.25,1.0,0.25))* m.getLength('arm'),
                    mass = m.getWeight('arm'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='arm_left',
                    bbox=array((0.25,1.0,0.25))* m.getLength('arm'),
                    mass = m.getWeight('arm'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='forearm_right',
                    bbox=array((0.25,1.0,0.25))* m.getLength('forearm'),
                    mass = m.getWeight('forearm'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='forearm_left',
                    bbox=array((0.25,1.0,0.25))* m.getLength('forearm'),
                    mass = m.getWeight('forearm'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='thigh_right',
                    bbox=array((0.25,1.0,0.25))* m.getLength('thigh'),
                    mass = m.getWeight('thigh'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='thigh_left',
                    bbox=array((0.25,1.0,0.25))* m.getLength('thigh'),
                    mass = m.getWeight('thigh'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='leg_right',
                    bbox=array((0.25,1.0,0.25))* m.getLength('leg'),
                    mass = m.getWeight('leg'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                ),
                ClimberPart(
                    name='leg_left',
                    bbox=array((0.25,1.0,0.25))* m.getLength('leg'),
                    mass = m.getWeight('leg'),
                    refRot=identity(3),
                    shape=self.PartShape.Cylinder,
                    jointsId=[]
                )]

        self.nParts = len(self.parts)

        ip = dict( (p.name, i) for i,p in enumerate(self.parts) )

        # WARNING : joint axes are not set yet, nor stops !!!

        self.joints = [
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['lbody'], ip['ubody']),
                    relAnchors=(array((0.0, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['ubody'], ip['head']),
                    relAnchors=(array((0.0, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['ubody'], ip['arm_right']),
                    relAnchors=(array((0.5, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['ubody'], ip['arm_left']),
                    relAnchors=(array((-0.5, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Hinge,
                    bodies=(ip['arm_right'], ip['forearm_right']),
                    relAnchors=(array((0.0, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Hinge,
                    bodies=(ip['arm_left'], ip['forearm_left']),
                    relAnchors=(array((0.0, 0.5, 0.0)), array((0.0, -0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['lbody'], ip['thigh_right']),
                    relAnchors=(array((0.25, -0.5, 0.0)), array((0.0, 0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Ball,
                    bodies=(ip['lbody'], ip['thigh_left']),
                    relAnchors=(array((-0.25, -0.5, 0.0)), array((0.0, 0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Hinge,
                    bodies=(ip['thigh_right'], ip['leg_right']),
                    relAnchors=(array((0.0, -0.5, 0.0)), array((0.0, 0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
                ),
                ClimberJoint(
                    freedom=self.JointType.Hinge,
                    bodies=(ip['thigh_left'], ip['leg_left']),
                    relAnchors=(array((0.0, -0.5, 0.0)), array((0.0, 0.5, 0.0))),
                    relAxes=(array((0.0, 0.0, 1.0)), array((0.0, 1.0, 0.0))),
                    stops=(-pi/2, pi/2, -pi/2, pi/2, -pi/2, pi/2)
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

    def getMass(self):
        return self.morphology.getWeight('total')
