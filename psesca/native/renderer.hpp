#ifndef _RENDERER_HPP
#define _RENDERER_HPP


#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>

#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>

#include <glm/mat4x4.hpp>

#include <string.h>
#include <fstream>
#include <vector>

#include "route.hpp"

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
		void initGeoms();
		void printGLError();
		void printEGLError();
		void printGLDebug();
	

		const Route * route;

		int width;
		int height;
		GLsizei sampling;

		EGLDisplay display;
		EGLContext context;
		GLuint framebuffer;
		GLuint renderbuffer;
		GLuint rb_framebuffer, rb_renderbuffer;
		GLuint depthbuffer;
		GLuint vertexShader;
		GLuint fragmentShader;
		GLuint program;

		GLuint routeArray, routeBuffer, routeNormalsBuffer;
		std::vector<unsigned short> routeStripsIndexes;
		std::vector<GLsizei> routeStripsCount;
		unsigned short ** routeStripsFirst;

		GLuint cylArray, cylBuffer, cylNormalsBuffer;
		GLsizei cylCounts[3];
		unsigned short cylFirsts[3];

};

#endif // _RENDERER_HPP
