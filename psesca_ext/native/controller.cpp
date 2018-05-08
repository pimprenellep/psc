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


float Controller::sumphi(struct Stance stance, float kro, struct Route route, struct MechState startState) //première partie de l'équation
{
	Position poslf = simulator->getPosition(Morphology::LEG_LEFT);
	Position poslh = simulator->getPosition(Morphology::FOREARM_LEFT);
	Position posrf = simulator->getPosition(Morphology::LEG_RIGHT);
	Position posrh = simulator->getPosition(Morphology::FOREARM_RIGHT);
	float philfDist = (stance.lf == -1 ? 0 : 1)*((pow(route.getHolds()[stance.lf].x-(poslf.x),2))+pow(route.getHolds()[stance.lf].y-(poslf.y),2)+ pow((poslf.z), 2));
	float phirfDist = (stance.rf == -1 ? 0 : 1)*((pow(route.getHolds()[stance.rf].x - (posrf.x), 2)) + pow(route.getHolds()[stance.rf].y - (posrf.y), 2) + pow((posrf.z), 2));
	float philhDist = (stance.lh == -1 ? 0 : 1)*((pow(route.getHolds()[stance.lh].x - (poslh.x), 2)) + pow(route.getHolds()[stance.lh].y - (poslh.y), 2) + pow((poslh.z), 2));
	float phirhDist = (stance.rh == -1 ? 0 : 1)*((pow(route.getHolds()[stance.rh].x - (posrh.x), 2)) + pow(route.getHolds()[stance.rh].y - (posrh.y), 2) + pow((posrh.z), 2));
	
	return((1 / kro)*(philfDist + phirfDist + philhDist + phirhDist));
}

float Controller::com(struct Stance stance, float kcom, struct MechState startState)
{

	return(1 / kcom);
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

