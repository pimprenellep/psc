#include "route.hpp"

Route::Route(int n, struct Hold *h) :
	nHolds(n),
	holds(h)
{
}

Route::~Route()
{
	delete holds;
}

const Hold * Route::getHolds() const
{
	return holds;
}
