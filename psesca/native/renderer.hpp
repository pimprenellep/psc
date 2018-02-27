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
		void initContext();
		void draw();
		void loadShaders();
		void initProjection();
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
		GLuint framebuffer;
		GLuint renderbuffer;
		GLuint vertexShader;
		GLuint fragmentShader;
		GLuint program;
};

#endif // _RENDERER_HPP
