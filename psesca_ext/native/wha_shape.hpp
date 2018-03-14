#ifndef _WHA_SHAPE_HPP
#define _WHA_SHAPE_HPP

#include "shape.hpp"

/// Simple width-height-area description of a hold
class WHAShape : public Shape {
	public:
		WHAShape(float width, float height, float area);
		virtual void getStrips(
				std::vector<GLfloat> &stripsComponents,
				std::vector<GLfloat> &stripsNormals,
				std::vector<unsigned short> &stripsIndexes,
				std::vector<GLsizei> &stripsCount,
				glm::mat4 &trans) const;
		virtual ~WHAShape();
	private:
		float width;
		float height;
		float area;
};

#endif // _WHA_SHAPE_HPP
