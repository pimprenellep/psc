#ifndef _MORPHOLOGY_HPP
#define _MORPHOLOGY_HPP

class Morphology {
	public:
		enum Part { LBODY, UBODY, HEAD,
			ARM_RIGHT, ARM_LEFT,
			FOREARM_RIGHT, FOREARM_LEFT,
			THIGH_RIGHT, THIGH_LEFT,
			LEG_RIGHT, LEG_LEFT, N_PARTS };

		Morphology(float height, float mass);
		float getHeight() const;
		float getLength(Part part) const;
		float getMass() const;
		float getMass(Part part) const;
	private:
		float mass, height;
		float relLength[N_PARTS];
		float relMass[N_PARTS];
};

#endif // _MORPHOLOGY_HPP
