#include "climbermodel.hpp"

#include "climbermodel_tables.hpp"

ClimberModel::ClimberModel(Morphology const *m) :
	morphology(m), nParts(Morphology::N_PARTS), nJoints(Morphology::N_PARTS - 1)
{
	int i = 0;
	components = (struct ClimberComponents){.parts = parts, .nParts = nParts,
			.joints = joints, .nJoints = nJoints};
#define AI(...) {__VA_ARGS__}
#define X(PART, BBOX ) \
	parts[Morphology::PART] = (struct ClimberPart){	\
		.bbox = BBOX,				\
		.mass = morphology->getMass(Morphology::PART),	\
		.shape = ClimberModel::PS_CYLINDER,	\
		.nJoints = 0,				\
		.joints = 0				\
	};
	CLIMBERMODEL_PARTS_TABLE
#undef X

#define X(TYPE, PART1, PART2, RELANCHOR1, RELANCHOR2, RELAXIS1, RELAXIS2, STOPS) \
	joints[i++] = (struct ClimberJoint){			\
		.type = TYPE,			\
		.parts = {Morphology::PART1, Morphology::PART2},		\
		.relAnchors = { RELANCHOR1, RELANCHOR2 }, \
		.relAxes = { RELAXIS1, RELAXIS2 },	\
		.stops = STOPS 	\
	};
	CLIMBERMODEL_JOINTS_TABLE
#undef X

}

ClimberModel::ClimberComponents const& ClimberModel::getComponents() const
{
	return components;
}

float ClimberModel::getMass() const
{
	return morphology->getMass();
}
