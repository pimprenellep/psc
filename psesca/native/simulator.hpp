#ifndef _SIMULATOR_HPP
#define _SIMULATOR_HPP

#include <iostream>
#include <gsl/gsl_const_mksa.h>
#include <ode/ode.h>


#include "climbermodel.hpp"

class Simulator {
	public:
		Simulator();
		~Simulator(); 
		void addClimber(ClimberModel const * m);
		void dumpFromOde() const;
		bool tests() const;

	private:
		dWorldID world;
		ClimberModel const * model;
		struct ClimberModel::ClimberComponents climber;
};

#endif // _SIMULATOR_HPP
