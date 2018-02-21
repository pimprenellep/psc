#ifndef _CONTROLLER_HPP
#define _CONTROLLER_HPP

#include "climbermodel.hpp"
#include "simulator.hpp"

class Controller {
	public:
		Controller(ClimberModel const * climber);
		~Controller();
		bool tests() const;
	private:
		ClimberModel const * climber;
		Simulator * simulator;
};

#endif // _CONTROLLER_HPP
