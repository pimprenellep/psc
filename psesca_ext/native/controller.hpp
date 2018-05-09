#ifndef _CONTROLLER_HPP
#define _CONTROLLER_HPP

#include "simulator.hpp"
#include "climbermodel.hpp"
#include "stancegraph.hpp"

/// Main class of the move generator
class Controller {
	public:
		Controller(ClimberModel const * climber, StanceGraph const * stanceGraph);
		~Controller();
		bool tests() const;
		/// Main function : tries to do a move
		float tryStep(struct Stance startStance, struct MechState startState, struct Stance endStance, struct MovePlan moveplan);
	private:
		ClimberModel const * climber;
		StanceGraph const * stanceGraph;
		Simulator * simulator;
		Route const * route;
		float sumphi(struct Stance stance, float kro, struct MechState startState);
		float com(struct Stance stance, float kcom, struct MechState startState);
		float cost(double const *x, unsigned long dim);
		int optLoop();
};

#endif // _CONTROLLER_HPP
