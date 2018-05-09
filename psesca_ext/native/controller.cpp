#include "controller.hpp"
#include "cmaes_interface.h"

const int T = 10; // N=t/dt
const int dt = 2;
const int J = 10; // J = nombre de joints
const int X = 3; //X = nombre de dimensions

Stance startStance;
Stance endStance;
MechState startState;// à définir !!


Controller::Controller(ClimberModel const * c, StanceGraph const * sg):
	climber(c),
	stanceGraph(sg)
{
	route = sg->getRoute();
	simulator = new Simulator(route);
	simulator->addClimber(climber);
}
//simulate the move and calculate the cost
float Controller::tryStep(struct Stance startStance, struct MechState startState, struct Stance endStance, struct MovePlan moveplan)
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

	simulator->move(dt, T , moveplan);
	return sumphi(startStance, kro, startState);//manque les autres membres de la somme

	// TODO : mechState has to contain rh, rf, lh with the 

}
//optimisated function
float Controller::cost(double const *x, unsigned long dim)
{
	unsigned k = 0;
	float c = 0;
	for(int t=0; t<T; t++) {
		MovePlan moveplan;
		for (int m = 0; m < J; m++) {
			for (int x = 0; x < 3; x++) {
				moveplan.targetVelocities[m][x] = x < -((3 * J*t) + 3 * m + x);//pour l'instant on ne tient pas compte des degrés de liberté :)
			}
		}
		c = c + tryStep(startStance, startState, endStance,moveplan);
	}
	return c;
}

//first term of the optimisated function
float Controller::sumphi(struct Stance stance, float kro, struct MechState startState) //première partie de l'équation
{
	Position poslf = simulator->getPosition(Morphology::LEG_LEFT);
	Position poslh = simulator->getPosition(Morphology::FOREARM_LEFT);
	Position posrf = simulator->getPosition(Morphology::LEG_RIGHT);
	Position posrh = simulator->getPosition(Morphology::FOREARM_RIGHT);
	float philfDist = (stance.lf == -1 ? 0 : 1)*((pow((route->getHolds())[stance.lf].x-(poslf.x),2))+pow((route->getHolds())[stance.lf].y-(poslf.y),2)+ pow((poslf.z), 2));
	float phirfDist = (stance.rf == -1 ? 0 : 1)*((pow((route->getHolds())[stance.rf].x - (posrf.x), 2)) + pow((route->getHolds())[stance.rf].y - (posrf.y), 2) + pow((posrf.z), 2));
	float philhDist = (stance.lh == -1 ? 0 : 1)*((pow((route->getHolds())[stance.lh].x - (poslh.x), 2)) + pow((route->getHolds())[stance.lh].y - (poslh.y), 2) + pow((poslh.z), 2));
	float phirhDist = (stance.rh == -1 ? 0 : 1)*((pow((route->getHolds())[stance.rh].x - (posrh.x), 2)) + pow((route->getHolds())[stance.rh].y - (posrh.y), 2) + pow((posrh.z), 2));
	
	return((1 / kro)*(philfDist + phirfDist + philhDist + phirhDist));
}
//second term
float Controller::com(struct Stance stance, float kcom, struct MechState startState)
{

	return(1 / kcom);
}


/* the optimization loop */
int Controller::optLoop() {
	cmaes_t evo; /* an CMA-ES type struct or "object" */
	double *arFunvals, *const*pop, *xfinal;
	int i;

	/* Initialize everything into the struct evo, 0 means default */
	arFunvals = cmaes_init(&evo, 0, NULL, NULL, 0, 0, "cmaes_initials.par");
	printf("%s\n", cmaes_SayHello(&evo));
	cmaes_ReadSignals(&evo, "cmaes_signals.par");  /* write header and initial values */

												   /* Iterate until stop criterion holds */
	while (!cmaes_TestForTermination(&evo))
	{
		/* generate lambda new search points, sample population */
		pop = cmaes_SamplePopulation(&evo); /* do not change content of pop */

											/* Here we may resample each solution point pop[i] until it
											becomes feasible. function is_feasible(...) needs to be
											user-defined.
											Assumptions: the feasible domain is convex, the optimum is
											not on (or very close to) the domain boundary, initialX is
											feasible and initialStandardDeviations are sufficiently small
											to prevent quasi-infinite looping. */
											/* for (i = 0; i < cmaes_Get(&evo, "popsize"); ++i)
											while (!is_feasible(pop[i]))
											cmaes_ReSampleSingle(&evo, i);
											*/

											/* evaluate the new search points using fitfun */
		for (i = 0; i < cmaes_Get(&evo, "lambda"); ++i) {
			arFunvals[i] = cost(pop[i], (int)cmaes_Get(&evo, "dim"));
		}

		/* update the search distribution used for cmaes_SamplePopulation() */
		cmaes_UpdateDistribution(&evo, arFunvals);

		/* read instructions for printing output or changing termination conditions */
		cmaes_ReadSignals(&evo, "cmaes_signals.par");
		fflush(stdout); /* useful in MinGW */
	}
	printf("Stop:\n%s\n", cmaes_TestForTermination(&evo)); /* print termination reason */
	cmaes_WriteToFile(&evo, "all", "allcmaes.dat");         /* write final results */

															/* get best estimator for the optimum, xmean */
	xfinal = cmaes_GetNew(&evo, "xmean"); /* "xbestever" might be used as well */
	cmaes_exit(&evo); /* release memory */

					  /* do something with final solution and finally release memory */
	free(xfinal);

	return 0;
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

