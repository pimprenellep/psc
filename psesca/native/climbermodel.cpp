#include "climbermodel.hpp"

#include <algorithm>
#include "climbermodel_tables.hpp"

ClimberModel::ClimberModel(Morphology const *m) :
	morphology(m), nParts(Morphology::N_PARTS), nJoints(Morphology::N_PARTS - 1)
{
	partsJoints = new int[nJoints * 2];
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
		;
#undef X
	for(int i = 0; i < components.nParts; i++) {
		float length = morphology->getLength(static_cast<Morphology::Part>(i));
		for(int j = 0; j < 3; j++) {
			parts[i].bbox[j] *= length;
		}
	}

#define X(TYPE, PART1, PART2, RELANCHOR1, RELANCHOR2, RELAXIS1, RELAXIS2, STOPS) \
	joints[i++] = (struct ClimberJoint){			\
		.type = TYPE,			\
		.parts = {Morphology::PART1, Morphology::PART2},		\
		.relAnchors = { RELANCHOR1, RELANCHOR2 }, \
		.relAxes = { RELAXIS1, RELAXIS2 },	\
		.stops = STOPS 	\
	};
	CLIMBERMODEL_JOINTS_TABLE
		;
#undef X
	for(int j = 0; j < nJoints; j++) {
		parts[joints[j].parts[0]].nJoints++;
		parts[joints[j].parts[1]].nJoints++;
	}
	std::fill(partsJoints, partsJoints + 2*nJoints, -1);
	int * ownJoints = partsJoints;
	for(int i = 0; i < nParts; i++) {
		parts[i].joints = ownJoints;
		ownJoints += parts[i].nJoints;
	}
	for(int j = 0; j < nJoints; j++) {
		for(int jip = 0; jip < 2; jip++) {
			ownJoints = parts[joints[j].parts[jip]].joints;
			while(*ownJoints != -1)
				ownJoints++;
			*ownJoints = j;
		}
	}
}

ClimberModel::~ClimberModel()
{
	delete[] partsJoints;
}

ClimberModel::ClimberComponents const& ClimberModel::getComponents() const
{
	return components;
}

float ClimberModel::getMass() const
{
	return morphology->getMass();
}
