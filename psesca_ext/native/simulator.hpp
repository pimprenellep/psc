#ifndef _SIMULATOR_HPP
#define _SIMULATOR_HPP

#include "renderer.hpp"

#include <iostream>
#include <ode/ode.h>


#include "climbermodel.hpp"
#include "route.hpp"

/// Full state of the climber at a given time
/** Values are pointers to buffers containing a copy of the simulator internal
 *  data, and can be used to save and load states of the simulator.
 */
struct MechState {
	const dVector3* positions;
	const dMatrix3* rotations;
};

struct Position {
	float x;
	float y;
	float z;
};

struct MovePlan {
	/** Array of size nJoints, whose components are arrays of reals of size
	  * matching the degree of freedom of the joint
	  */
	dReal ** targetVelocities;
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

		/// Get a copy of the mechanical state for the engine
		/** Must be freed with freeMechState after use
		 */
		struct MechState getMechState() const;

		Position getPosition(Morphology::Part part) const;
		//gives the position of the extremities


	
		void freeMechState(struct MechState& mechState) const;
		void loadMechState(const struct MechState& mechState);

		/// Simulate a portion of a move
		void move(float dt, int divs, struct MovePlan movePlan);

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
