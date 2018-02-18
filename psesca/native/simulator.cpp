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





