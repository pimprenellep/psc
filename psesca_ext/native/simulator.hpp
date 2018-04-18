#ifndef _SIMULATOR_HPP
#define _SIMULATOR_HPP

#include "renderer.hpp"

#include <iostream>
#include <ode/ode.h>


#include "climbermodel.hpp"
#include "route.hpp"

/// Full state of the climber at a given time
/** Values are pointers to the engine's internal data structures,
 *  and the content can change with any call to a simulation method.
 */
struct MechState {
	const dVector3* positions;
};

struct Position {
	float x;
	float y;
	float z;
};


/// Physical engine wrapper
class Simulator {
	public:
		// Init the physical engine for the given route
		Simulator(Route const * route);
		~Simulator();
		float positionlh[2];

		/// Adds the climber to the underlying engine
		/** Warning : this function is not yet reentrant
		 */
		void addClimber(ClimberModel const * m);
		/// Get the mechanical state for the engine
		struct MechState getMechState() const;

		Position getPositionlf() const;
		
		//Position * getPositionrf;
		//Position * getPositionlh;
		//Position * getPositionrh;
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
