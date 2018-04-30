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
		void tryStep(struct Stance startStance, struct MechState startState, struct Stance endStance);
	private:
		ClimberModel const * climber;
		StanceGraph const * stanceGraph;
		Simulator * simulator;
		float sumphi(struct Stance stance, float kro, struct Route route, struct MechState startState);
};

#endif // _CONTROLLER_HPP
