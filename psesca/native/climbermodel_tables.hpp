#include <math.h>

//	  PART, 	bbox
#define CLIMBERMODEL_PARTS_TABLE \
	X(LBODY,	AI(1.0, 1.0, 1.0))	\
	X(UBODY,	AI(1.0, 1.0, 1.0))	\
	X(HEAD,		AI(1.0, 1.0, 1.0))	\
	X(ARM_RIGHT,	AI(0.25, 1.0, 0.25))	\
	X(ARM_LEFT,	AI(0.25, 1.0, 0.25))	\
	X(FOREARM_LEFT,	AI(0.25, 1.0, 0.25))	\
	X(FOREARM_RIGHT,AI(0.25, 1.0, 0.25))	\
	X(THIGH_RIGHT,	AI(0.25, 1.0, 0.25))	\
	X(THIGH_LEFT,	AI(0.25, 1.0, 0.25))	\
	X(LEG_RIGHT,	AI(0.25, 1.0, 0.25))	\
	X(LEG_LEFT,	AI(0.25, 1.0, 0.25))

// type, part1, part2, relAnchor1, relAnchor2, relAxis1, relAxis2, stops
#define CLIMBERMODEL_JOINTS_TABLE \
	X(JT_BALL, LBODY, UBODY, AI(0.0, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_BALL, UBODY, HEAD, AI(0.0, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_BALL, UBODY, ARM_RIGHT, AI(0.5, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_BALL, UBODY, ARM_LEFT, AI(-0.5, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_HINGE, ARM_RIGHT, FOREARM_RIGHT, AI(0.0, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_HINGE, ARM_LEFT, FOREARM_LEFT, AI(0.0, 0.5, 0.0), AI(0.0, -0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_BALL, LBODY, THIGH_RIGHT, AI(0.25, -0.5, 0.0), AI(0.0, 0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_BALL, LBODY, THIGH_LEFT, AI(-0.25, -0.5, 0.0), AI(0.0, 0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_HINGE, THIGH_RIGHT, LEG_RIGHT, AI(0.0, -0.5, 0.0), AI(0.0, 0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))	\
	X(JT_HINGE, THIGH_LEFT, LEG_LEFT, AI(0.0, -0.5, 0.0), AI(0.0, 0.5, 0.0), AI(0.0, 0.0, 1.0), AI(0.0, 1.0, 0.0), AI(-M_PI/2, M_PI/2, -M_PI/2, M_PI/2, -M_PI/2, M_PI/2))
