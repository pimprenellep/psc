#ifndef _CLIMBERMODEL_HPP
#define _CLIMBERMODEL_HPP

#include "morphology.hpp"

class ClimberModel {
	public:
		enum PartShape { PS_CYLINDER };

		enum JointType { JT_HINGE, JT_BALL };

		struct ClimberPart {
			float bbox[3];
			float mass;
			enum PartShape shape;
			int nJoints;
			int * joints;
		};


		struct ClimberJoint {
			enum JointType type;
			enum Morphology::Part parts[2];
			float relAnchors[2][3];
			float relAxes[2][3];
			float stops[3][2];
		};
	
		struct ClimberComponents {
			struct ClimberPart const * parts;
			int nParts;
			struct ClimberJoint const * joints;
			int nJoints;
		};

		ClimberModel(Morphology const *m);
		ClimberComponents const& getComponents() const;
		float getMass() const;
	private:
		Morphology const * morphology;
		struct ClimberPart parts[Morphology::N_PARTS];
		int nParts;
		struct ClimberJoint joints[Morphology::N_PARTS - 1];
		int nJoints;
		struct ClimberComponents components;
};

#endif // _CLIMBERMODEL_HPP
