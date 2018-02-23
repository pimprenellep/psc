#ifndef _RENDERER_HPP
#define _RENDERER_HPP

#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>

#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>

#include <fstream>

class Renderer {
	public:
	       	Renderer();
		~Renderer();
		bool saveToFile(const char *file);
	private:
		void printGLError();
		void printEGLError();
	
		int width;
		int height;
		EGLDisplay display;
		EGLContext context;
		EGLSurface pbuffer;
};

#endif // _RENDERER_HPP
