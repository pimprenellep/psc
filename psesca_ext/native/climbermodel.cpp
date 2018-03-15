#include "climbermodel.hpp"

#include <algorithm>
#include "climbermodel_tables.hpp"

ClimberModel::ClimberModel(Morphology const *m) :
	morphology(m), nParts(Morphology::N_PARTS), nJoints(Morphology::N_PARTS - 1)
{
	partsJoints = new int[nJoints * 2];
	int i = 0;
	components.parts = parts;
	components.nParts = nParts;
	components.joints = joints;
	components.nJoints = nJoints;

#define AI(...) {__VA_ARGS__}
#define X(PART, BBOX ) \
		{ float bbox[3] = BBOX;	\
		std::copy(bbox, bbox + 3, &(parts[Morphology::PART].bbox[0])); }				\
		parts[Morphology::PART].mass = morphology->getMass(Morphology::PART);	\
		parts[Morphology::PART].shape = ClimberModel::PS_CYLINDER;	\
		parts[Morphology::PART].nJoints = 0;				\
		parts[Morphology::PART].joints = 0;
	CLIMBERMODEL_PARTS_TABLE
		;
#undef X
	for (int i = 0; i < components.nParts; i++) {
		float length = morphology->getLength(static_cast<Morphology::Part>(i));
		for (int j = 0; j < 3; j++) {
			parts[i].bbox[j] *= length;
		}
	}

#define X(TYPE, PART1, PART2, RELANCHOR1, RELANCHOR2, RELAXIS1, RELAXIS2, STOPS) \
	joints[i].type = TYPE;			\
	joints[i].parts[0] = Morphology::PART1;	\
	joints[i].parts[1] =  Morphology::PART2;		\
	{ \
		float  rela1[3] = RELANCHOR1;		\
		float  rela2[3] = RELANCHOR1;		\
		std::copy(rela1, rela1+3, &(joints[i].relAnchors[0][0])); \
		std::copy(rela2, rela2+3, &(joints[i].relAnchors[1][0])); \
	} \
	{ \
		float  rela1[3] = RELAXIS1;		\
		float  rela2[3] = RELAXIS1;		\
		std::copy(rela1, rela1+3, &(joints[i].relAxes[0][0])); \
		std::copy(rela2, rela2+3, &(joints[i].relAxes[1][0])); \
	} \
	{ \
		float stops[6] = STOPS; \
		std::copy(stops, stops + 6, &(joints[i].stops[0][0])); \
	} \
	i++;

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
