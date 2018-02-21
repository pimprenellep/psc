#include "simulator.hpp"

Simulator::Simulator() :
	world(dWorldCreate()),
	model(0),
	ODEParts(0),
	ODEJoints(0)
{
	climber = (struct ClimberModel::ClimberComponents){0, 0, 0, 0};
	dWorldSetGravity(world, 0.0, - GSL_CONST_MKSA_GRAV_ACCEL, 0.0);
}

Simulator::~Simulator()
{
	delete[] ODEParts;
	delete[] ODEJoints;
	dWorldDestroy(world);
}

void Simulator::addClimber(ClimberModel const * m)
{
	model = m;
	climber = m->getComponents();

	ODEParts = new dBodyID[climber.nParts];
	ODEJoints = new dJointID[climber.nJoints];
	dMass mass;

	for(int ip = 0; ip < climber.nParts; ip++) {
		struct ClimberModel::ClimberPart const& p = climber.parts[ip];
		ODEParts[ip] = dBodyCreate(world);
		switch(p.shape) {
		case ClimberModel::PS_CYLINDER:
			dMassSetCylinder(&mass, p.mass, 2,
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

void Simulator::dumpFromOde() const
{
	std::cout << "Position of all parts:" << std::endl;	
	for(int ip = 0; ip < climber.nParts; ip++) {
		const dReal * p = dBodyGetPosition(ODEParts[ip]);
		std::cout << "Part " << ip << ": "
			<< p[0] << ", " << p[1] << ", " << p[2]
			<< std::endl;
	}
}

bool Simulator::tests() const
{
	dumpFromOde();
	return false;
}





