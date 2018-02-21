#include "controller.hpp"

Controller::Controller(ClimberModel const * c) :
	climber(c),
	simulator(new Simulator())
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

