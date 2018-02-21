#include "morphology.hpp"

Morphology::Morphology(float h, float m) :
	height(h), mass(m)
{
#define X(PART, MASS, LENGTH) \
	relMass[PART] = MASS;	\
	relLength[PART] = LENGTH;

#define BIODATA
	X(HEAD,			0.09,	0.1)	\
	X(UBODY,		0.24,	0.1)	\
	X(LBODY,		0.24,	0.11)	\
	X(FOREARM_RIGHT,	0.024,	0.22)	\
	X(FOREARM_LEFT,		0.024,	0.22)	\
	X(ARM_RIGHT,		0.028,	0.17)	\
	X(ARM_LEFT,		0.028,	0.17)	\
	X(THIGH_RIGHT,		0.1,	0.246)	\
	X(THIGH_LEFT,		0.1,	0.246)	\
	X(LEG_RIGHT,		0.063,	0.0325)	\
	X(LEG_LEFT,		0.063,	0.0325)

	BIODATA

#undef X
}

float Morphology::getLength(Morphology::Part part) const
{
	return relLength[part] * height;
}

float Morphology::getMass(Morphology::Part part) const
{
	return relMass[part] * mass;
}

float Morphology::getMass() const
{
	return mass;
}

float Morphology::getHeight() const
{
	return height;
}
