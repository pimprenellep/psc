#ifndef _RENDERER_HPP
#define _RENDERER_HPP

#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>

#include <GL/gl.h>
#include <GL/glext.h>

class Renderer {
	public:
	       	Renderer();
		~Renderer();
	private:
		EGLDisplay display;
		EGLContext context;
};

#endif // _RENDERER_HPP
