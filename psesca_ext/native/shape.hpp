#ifndef _SHAPE_HPP	
#define _SHAPE_HPP

#include "glcontext.hpp"

#include <glm/mat4x4.hpp>

#include <vector>

/// Abstract shape of a hold
/** Since the shape can be represented in many different ways,
 *  all that depends on the shape should be encapsulated in a subclass a this one.
 */
class Shape {
	public:
		virtual void getStrips(
				std::vector<GLfloat> &stripsComponents,
				std::vector<GLfloat> &stripsNormals,
				std::vector<unsigned short> &stripsIndexes,
				std::vector<GLsizei> &stripsCount,
				glm::mat4 &trans) const = 0;

		virtual ~Shape();
};

#endif // _SHAPE_HPP

