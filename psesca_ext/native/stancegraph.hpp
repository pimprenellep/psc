#ifndef _STANCE_GRAPH_HPP
#define _STANCE_GRAPH_HPP

#include "route.hpp"

struct Stance {
	int lf;
	int rf;
	int lh;
	int rh;
};

class StanceGraph {
	public:
		StanceGraph(const Route *route);
		const Route *getRoute() const;
	private:
		const Route *route;
		
};

#endif // _STANCE_GRAPH_HPP
