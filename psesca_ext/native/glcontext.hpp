#ifndef _GLCONTEXT_HPP
#define _GLCONTEXT_HPP

#ifdef WITH_EGL
#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>
#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>
#endif

#ifdef WITH_WGL
#include <windows.h>
#include "glew.h"
#endif

class GLContext {
public:
	GLContext();
	~GLContext();
	bool isValid();
#ifdef WITH_EGL
	void printEGLError() const;
#endif

private:
#ifdef WITH_EGL
	EGLDisplay display;
	EGLContext context;
#endif
};
#endif // _GL_CONTEXT_HPP