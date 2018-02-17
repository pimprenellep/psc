//	  PART, 	bbox
#define CLIMBERMODEL_PARTS_TABLE \
	X(LBODY,	({1.0, 1.0, 1.0}))	\
	X(UBODY,	({1.0, 1.0, 1.0}))	\
	X(HEAD,		({1.0, 1.0, 1.0}))	\
	X(ARM_RIGHT,	({0.25, 1.0, 0.25}))	\
	X(ARM_LEFT,	({0.25, 1.0, 0.25}))	\
	X(FOREARM_LEFT,	({0.25, 1.0, 0.25}))	\
	X(FOREARM_RIGHT,({0.25, 1.0, 0.25}))	\
	X(THIGH_RIGHT,	({0.25, 1.0, 0.25}))	\
	X(THIGH_LEFT,	({0.25, 1.0, 0.25}))	\
	X(LEG_RIGHT,	({0.25, 1.0, 0.25}))	\
	X(LEG_LEFT,	({0.25, 1.0, 0.25}))

// type, part1, part2, relAnchor1, relAnchor2, relAxis1, relAxis2, stops
#define CLIMBER_MODEL_JOINTS_TABLE \
	X(JT_BALL, LBODY, UBODY, ({0.0, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_BALL, UBODY, HEAD, ({0.0, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_BALL, UBODY, ARM_RIGHT, ({0.5, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_BALL, UBODY, ARM_LEFT, ({-0.5, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_HINGE, ARM_RIGHT, FOREARM_RIGHT, ({0.0, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_HINGE, ARM_LEFT, FOREARM_LEFT, ({0.0, 0.5, 0.0}), ({0.0, -0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_BALL, LBODY, THIGH_RIGHT, ({0.25, -0.5, 0.0}), ({0.0, 0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_BALL, LBODY, THIGH_LEFT, ({-0.25, -0.5, 0.0}), ({0.0, 0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_HINGE, THIGH_RIGHT, LEG_RIGHT, ({0.0, -0.5, 0.0}), ({0.0, 0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))	\
	X(JT_HINGE, THIGH_LEFT, LEG_LEFT, ({0.0, -0.5, 0.0}), ({0.0, 0.5, 0.0}), ({0.0, 0.0, 1.0}), ({0.0, 1.0, 0.0}), ({-PI/2, PI/2, -PI/2, PI/2, -PI/2, PI/2}))
