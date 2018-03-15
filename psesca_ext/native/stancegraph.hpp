#ifndef _STANCE_GRAPH_HPP
#define _STANCE_GRAPH_HPP

#include "route.hpp"

class StanceGraph {
	public:
		StanceGraph(const Route *route);
		const Route *getRoute() const;
	private:
		const Route *route;
		
};

#endif // _STANCE_GRAPH_HPP
