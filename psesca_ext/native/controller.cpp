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
	//route indique la voie qui est en train d'être analysée
	//put here the cost function
	float kdir;
	float kro;
	float kvelocity;
	float kpostureFree;
	float kpostureClimb;
	float kcom;
	float kforce;

	
	// TODO : mechState has to contain rh, rf, lh with the 

}

float Controller::sumphi(struct Stance stance, float kro, struct Route route, struct MechState startState) 
{
	Position poslf = simulator->getPositionlf();
	float philf = (stance.lf == -1 ? 0 : 1)*(pow(route.getHolds()[stance.lf].x-(poslf.x),2));
	float phirf = 0;
	float philh = 0;
	float phirh = 0;
	return((1 / kro)*(phirh + phirf + philh + phirh));
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
float pow(float a)
{
	return a * a;
}

Controller::~Controller()
{
	delete simulator;
}

