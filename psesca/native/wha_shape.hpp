#ifndef _WHA_SHAPE_HPP
#define _WHA_SHAPE_HPP

#include "shape.hpp"

/// Simple width-height-area description of a hold
class WHAShape : public Shape {
	public:
		WHAShape(float width, float height, float area);
		virtual void glDraw(float x, float y) const;
		virtual ~WHAShape();
	private:
		float width;
		float height;
		float area;
};

#endif // _WHA_SHAPE_HPP
