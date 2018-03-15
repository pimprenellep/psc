#ifndef _SIMULATOR_HPP
#define _SIMULATOR_HPP

#include "renderer.hpp"

#include <iostream>
#include <ode/ode.h>


#include "climbermodel.hpp"
#include "route.hpp"


class Simulator {
	public:
		Simulator(Route const * route);
		~Simulator(); 
		void addClimber(ClimberModel const * m);
		void dumpFromOde() const;
		bool tests() const;
		bool testFreeFall(float time, int divs, float tolerance) const;

	private:
		ClimberModel const * model;
		Route const * route;
		struct ClimberModel::ClimberComponents climber;
		dWorldID world;
		dBodyID * ODEParts;
		dJointID * ODEJoints;
		dJointID * ODEMotors;
		Renderer * renderer;
};

#endif // _SIMULATOR_HPP
