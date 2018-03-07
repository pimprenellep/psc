#include "route.hpp"

#include <cstdlib>

Route::Route(int n, struct Hold *h) :
	nHolds(n),
	holds(h)
{
}

Route::~Route()
{
	free(holds);
}

const Hold * Route::getHolds() const
{
	return holds;
}

const int Route::getNHolds() const
{
	return nHolds;
}
