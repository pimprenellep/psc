#ifndef _RENDERER_HPP
#define _RENDERER_HPP

#include "route.hpp"

#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>

#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>

#include <string.h>
#include <fstream>

class Renderer {
	public:
	       	Renderer(const Route *route);
		~Renderer();
		bool saveToFile(const char *file);
	private:
		void draw();
		void loadShaders();
		void loadRoute();
		void printGLError();
		void printEGLError();
		void printGLDebug();
	

		const Route * route;
		int width;
		int height;
		EGLDisplay display;
		EGLContext context;
		EGLSurface pbuffer;
};

#endif // _RENDERER_HPP
