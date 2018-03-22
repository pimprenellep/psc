#include "controller.hpp"

Controller::Controller(ClimberModel const * c, StanceGraph const * sg):
	climber(c),
	stanceGraph(sg)
{
	simulator = new Simulator(sg->getRoute());
	simulator->addClimber(climber);
}

void Controller::tryStep(struct Stance startStance, struct MechState startState, struct Stance endStance)
{
}

bool Controller::tests() const
{
	bool r = false;
	r = r || simulator->tests();
	if(r) {
		std::cout << "Controller tests failed." << std::endl;
	}
	return r;
}

Controller::~Controller()
{
	delete simulator;
}

