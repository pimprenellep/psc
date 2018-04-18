#include "simulator.hpp"

#include <iostream>
#include <algorithm>
const float g =  9.80665;

Simulator::Simulator(Route const* r) :
	model(0),
	route(r),
	ODEParts(0),
	ODEJoints(0),
	renderer(new Renderer(route))
{
	climber.parts = 0;
	climber.nParts = 0;
	climber.joints = 0;
	climber.nJoints = 0;

	dInitODE();
	world = dWorldCreate();
	dWorldSetGravity(world, 0.0, -g, 0.0);
}

Simulator::~Simulator()
{
	delete[] ODEParts;
	delete[] ODEJoints;
	delete[] ODEMotors;
	dWorldDestroy(world);
	delete renderer;
}

void Simulator::addClimber(ClimberModel const * m)
{
	model = m;
	climber = m->getComponents();

	ODEParts = new dBodyID[climber.nParts];
	ODEJoints = new dJointID[climber.nJoints];
	ODEMotors = new dJointID[climber.nJoints];
	dMass mass;

	for(int ip = 0; ip < climber.nParts; ip++) {
		struct ClimberModel::ClimberPart const& p = climber.parts[ip];
		ODEParts[ip] = dBodyCreate(world);
		switch(p.shape) {
		case ClimberModel::PS_CYLINDER:
			dMassSetCylinderTotal(&mass, p.mass, 2,
					0.5 * std::min(p.bbox[0], p.bbox[1]),
					p.bbox[1]);
			break;
		}
		dBodySetMass(ODEParts[ip], &mass);
	}

	
	for(int i = 0; i < climber.nJoints; i++) {
		struct ClimberModel::ClimberJoint const& j = climber.joints[i];
		switch(j.type) {
		case ClimberModel::JT_HINGE:
			ODEJoints[i] = dJointCreateHinge(world, 0);
			break;
		case ClimberModel::JT_BALL:
			ODEJoints[i] = dJointCreateBall(world, 0);
			break;
		}
		dJointAttach(ODEJoints[i],
				ODEParts[j.parts[0]], ODEParts[j.parts[1]]);
		//ODEMotors[i] = dJointCreateAMotor(world, 0);
		ODEMotors[i] = 0;
		/*
		   dJointAttach(ODEMotors[i],
				ODEParts[j.parts[0]], ODEParts[j.parts[1]]);
				*/
	}

	bool *closed = new bool[climber.nParts]{false};
	int *open = new int[climber.nParts];
	int top = 0;
	open[top++] = 0;

	while(top) {
		int ip1 = open[--top];
		closed[ip1] = true;

		struct ClimberModel::ClimberPart const& p1 = climber.parts[ip1];

		for(int p1ij = 0; p1ij < p1.nJoints ; p1ij++) {
			int ij = p1.joints[p1ij];
			struct ClimberModel::ClimberJoint const& j = climber.joints[ij];
			int ji1 = (j.parts[0] == ip1) ? 0 : 1;
			int ji2 = 1 - ji1;
			int ip2 = j.parts[ji2];

			if(closed[ip2])
				continue;
			open[top++] = ip2;

			struct ClimberModel::ClimberPart const& p2 = climber.parts[ip2];
			dReal relAnchor1[3];
			dReal relAnchor2[3];
			for(int d = 0; d < 3; d++) {
				relAnchor1[d] = p1.bbox[d] * j.relAnchors[ji1][d];
				relAnchor2[d] = p2.bbox[d] * j.relAnchors[ji2][d];
			}
			dVector3 anchor1, anchor2;
			dBodyGetRelPointPos(ODEParts[ip1], relAnchor1[0], relAnchor1[1], relAnchor1[2], anchor1);
			dBodyGetRelPointPos(ODEParts[ip2], relAnchor2[0], relAnchor2[1], relAnchor2[2], anchor2);
			dVector3 delta;
			for(int d = 0; d < 3; d++) {
				delta[d] = anchor1[d] - anchor2[d];
			}
			dBodySetPosition(ODEParts[ip2], delta[0], delta[1], delta[2]);
			switch(j.type) {
			case ClimberModel::JT_HINGE:
				dJointSetHingeAnchor(ODEJoints[ij], anchor1[0], anchor1[1], anchor1[2]);
				break;
			case ClimberModel::JT_BALL:
				dJointSetBallAnchor(ODEJoints[ij], anchor1[0], anchor1[1], anchor1[2]);
				break;
			}


		}

	}

	delete[] closed;
	delete[] open;
}

struct MechState Simulator::getMechState() const {
	struct MechState mechState;
	dVector3 *pos = new dVector3[climber.nParts];
	dMatrix3 *rot = new dMatrix3[climber.nParts];
	for(int ip = 0; ip < climber.nParts; ip++) {
		dBodyCopyPosition(ODEParts[ip], pos[ip]);
		dBodyCopyRotation(ODEParts[ip], rot[ip]);
	}
	mechState.positions = pos;
	mechState.rotations = rot;
	return mechState;
}

void Simulator::freeMechState(struct MechState& mechState) const {
	delete[] mechState.positions;
	delete[] mechState.rotations;
}

void Simulator::dumpFromOde() const
{
	std::cout << "Position of all parts:" << std::endl;	
	struct MechState mechState = getMechState();
	for(int ip = 0; ip < climber.nParts; ip++) {
		//const dReal * p = dBodyGetPosition(ODEParts[ip]);
		const dReal * p = mechState.positions[ip];
		std::cout << "Part " << ip << ": "
			<< p[0] << ", " << p[1] << ", " << p[2]
			<< std::endl;
	}
	freeMechState(mechState);
}

bool Simulator::tests() const
{
	bool failed = false;

	dumpFromOde();
	failed = failed || testFreeFall(100.0, 1e5, 1e-6);
	return false;
}

bool Simulator::testFreeFall(float time, int divs, float tolerance) const
{
	std::cout << "Test : free fall, time="<<time
		<<", divs="<<divs
		<<", tolerance="<<tolerance
		<< std::endl;

	float theo = -g * time * time / 2.0;
	Morphology::Part ref = Morphology::HEAD;
	dReal pos0[3];
	const dReal * pos = dBodyGetPosition(ODEParts[ref]);
	for(int d = 0; d < 3; d++) pos0[d] = pos[d];

	for(int i = 0; i < divs; i++) {
		dWorldStep(world, time/divs);
	}
	//pos = dBodyGetPosition(ODEParts[ref]);
	dReal delta[3];
	for(int d = 0; d < 3; d++) delta[d] = pos[d] - pos0[d];
	delta[1] -= theo;

	float err2 = 0;
	for(int d = 0; d < 3; d++) err2 += delta[d]*delta[d];
	err2 /= theo*theo;

	bool failed = (err2 > tolerance);
	std::cout << "Test free fall "
		<< (failed ? "failed" : "passed") << ". "
		"(err2="<<err2<<", "
		"tolerance="<<tolerance<<")"
		<<std::endl;
	return failed;
}







