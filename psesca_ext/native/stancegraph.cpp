#include "stancegraph.hpp"


StanceGraph::StanceGraph(const Route *r) :
	route(r)
{
}

const Route *
StanceGraph::getRoute() const 
{
	return route;
}
