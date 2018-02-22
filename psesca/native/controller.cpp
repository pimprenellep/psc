#include "controller.hpp"

Controller::Controller(ClimberModel const * c, StanceGraph const * sg):
	climber(c),
	stanceGraph(sg),
	simulator(new Simulator(sg->getRoute()))
{
	simulator->addClimber(climber);
}

Controller::~Controller()
{
	delete simulator;
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

