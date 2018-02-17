#include "simulator.hpp"

Simulator::Simulator() :
	world(dWorldCreate()),
	model(0),
	climber{0,0,0,0}
{
	dWorldSetGravity(world, 0.0, - GSL_CONST_MKSA_GRAV_ACCEL, 0.0);
}

Simulator::~Simulator()
{
	dWorldDestroy(world);
}

void Simulator::addClimber(ClimberModel const * m) {
	model = m;
	climber = m->getComponents();
}

void Simulator::dumpFromOde() const
{
	std::cout << "Nothing to dump from ODE." << std::endl;	
}

bool Simulator::tests() const
{
	dumpFromOde();
	return false;
}





