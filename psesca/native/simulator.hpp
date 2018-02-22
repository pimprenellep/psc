#ifndef _SIMULATOR_HPP
#define _SIMULATOR_HPP

#include <iostream>
#include <gsl/gsl_const_mksa.h>
#include <ode/ode.h>


#include "climbermodel.hpp"
#include "route.hpp"
#include "renderer.hpp"

class Simulator {
	public:
		Simulator(Route const * route);
		~Simulator(); 
		void addClimber(ClimberModel const * m);
		void dumpFromOde() const;
		bool tests() const;

	private:
		ClimberModel const * model;
		Route const * route;
		struct ClimberModel::ClimberComponents climber;
		dWorldID world;
		dBodyID * ODEParts;
		dJointID * ODEJoints;
		Renderer * renderer;
};

#endif // _SIMULATOR_HPP
