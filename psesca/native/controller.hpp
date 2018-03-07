#ifndef _CONTROLLER_HPP
#define _CONTROLLER_HPP

#include "climbermodel.hpp"
#include "stancegraph.hpp"
#include "simulator.hpp"

class Controller {
	public:
		Controller(ClimberModel const * climber, StanceGraph const * stanceGraph);
		~Controller();
		bool tests() const;
	private:
		ClimberModel const * climber;
		StanceGraph const * stanceGraph;
		Simulator * simulator;
};

#endif // _CONTROLLER_HPP
