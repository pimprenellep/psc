#ifndef _ROUTE_HPP
#define _ROUTE_HPP

#include "shape.hpp"

struct Hold {
	float x;
	float y;
	Shape *shape;
};

class Route {
	public:
		/// Constructor
		/* Route is responsible for recursively freeing holds.
		 */
		Route(int nHolds, struct Hold *holds);
		/// Destructor
		/* Frees the hold array but _not_ the shapes within.
		 */
		~Route();
		const Hold * getHolds() const;
	private:
		int nHolds;
		Hold *holds;
};

#endif // _ROUTE_HPP

