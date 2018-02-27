#ifndef _SHAPE_HPP	
#define _SHAPE_HPP

/// Abstract shape of a hold
/** Since the shape can be represented in many different ways,
 *  all that depends on the shape should be encapsulated in a subclass a this one.
 */
class Shape {
	public:
		/// Draw the hold in current OpenGL context
		virtual void glDraw(float x, float y) const = 0;
		virtual ~Shape();
};

#endif // _SHAPE_HPP

