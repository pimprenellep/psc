#include "renderer.hpp"

#include <iostream>
#include <cassert>


#define DIEIFN(ok, msg)		\
	if(!(ok)) {		\
		std::cerr << "Renderer : " msg << std::endl;	\
		printEGLError();				\
		return;						\
	}

#define ERRORS_EGL(X)	\
	X(EGL_SUCCESS)		\
	X(EGL_NOT_INITIALIZED)	\
	X(EGL_BAD_ACCESS)	\
	X(EGL_BAD_ALLOC)	\
	X(EGL_BAD_ATTRIBUTE)	\
	X(EGL_BAD_CONFIG)	\
	X(EGL_BAD_CONTEXT)	\
	X(EGL_BAD_CURRENT_SURFACE)	\
	X(EGL_BAD_DISPLAY)	\
	X(EGL_BAD_MATCH)	\
	X(EGL_BAD_NATIVE_PIXMAP)	\
	X(EGL_BAD_NATIVE_WINDOW)	\
	X(EGL_BAD_PARAMETER)	\
	X(EGL_BAD_SURFACE)	\
	X(EGL_CONTEXT_LOST)

void Renderer::printEGLError()
{
	EGLint err = eglGetError();

#define ERROR_CASE(E) \
	case E:		\
	std::cerr << "EGL error is " #E << std::endl; \
	break;

	switch(err) {
		ERRORS_EGL(ERROR_CASE)
	default:
		std::cerr << "Unknown EGL error : " << err << std::endl;
	}

#undef ERROR_CASE
}

#define ERRORS_GL(X)	\
	X(GL_NO_ERROR)	\
	X(GL_INVALID_ENUM)	\
	X(GL_INVALID_VALUE)	\
	X(GL_INVALID_OPERATION)	\
	X(GL_STACK_OVERFLOW)	\
	X(GL_STACK_UNDERFLOW)	\
	X(GL_OUT_OF_MEMORY)

void Renderer::printGLError()
{
	GLenum err = glGetError();

#define ERROR_CASE(E) \
	case E:		\
	std::cerr << "GL error is " #E << std::endl; \
	break;

	switch(err) {
		ERRORS_GL(ERROR_CASE)
	default:
		std::cerr << "Unknown GL error : " << err << std::endl;
	}

#undef ERROR_CASE
}
Renderer::Renderer() :
	display(EGL_NO_DISPLAY),
	context(EGL_NO_CONTEXT)
{
	EGLBoolean ok;

	std::cerr << eglQueryString(EGL_NO_DISPLAY, EGL_EXTENSIONS) << std::endl;

	EGLDeviceEXT devices[16];
	EGLint nDevices = 0;

	PFNEGLQUERYDEVICESEXTPROC eglQueryDevicesEXT =
		(PFNEGLQUERYDEVICESEXTPROC) eglGetProcAddress("eglQueryDevicesEXT");
	if(eglQueryDevicesEXT) {
		ok = eglQueryDevicesEXT(16, devices, &nDevices);
		DIEIFN(ok, "Cannot enumerate devices.");
	}

	std::cout << nDevices << " graphical devices found." << std::endl;


	PFNEGLGETPLATFORMDISPLAYEXTPROC eglGetPlatformDisplayEXT =
		(PFNEGLGETPLATFORMDISPLAYEXTPROC) eglGetProcAddress("eglGetPlatformDisplayEXT");
	assert(eglGetPlatformDisplayEXT);

	if(nDevices) {
		std::cout << "Devices found, trying to get device display." << std::endl;
		display = eglGetPlatformDisplayEXT(EGL_PLATFORM_DEVICE_EXT, EGL_DEFAULT_DISPLAY, 0);
	} else {
		std::cout << "No devices found, trying to get default display." << std::endl;
		//display = eglGetPlatformDisplayEXT(EGL_PLATFORM_GBM_MESA, EGL_DEFAULT_DISPLAY, 0);
		display = eglGetDisplay(EGL_DEFAULT_DISPLAY);
	}
	if(display == EGL_NO_DISPLAY) {
		std::cerr << "Renderer : cannot get display." << std::endl;
		return;
	}

	EGLint major, minor;
	ok = eglInitialize(display, &major, &minor);
	if(!ok) {
		std::cerr << "Renderer : cannot initialize display." << std::endl;
		return;
	}

	std::cerr << eglQueryString(display, EGL_VENDOR) << std::endl;
	std::cerr << eglQueryString(display, EGL_CLIENT_APIS) << std::endl;
	std::cerr << eglQueryString(display, EGL_EXTENSIONS) << std::endl;

	ok = eglBindAPI(EGL_OPENGL_API);
	DIEIFN(ok, "Renderer : cannot bind api.");

	EGLConfig config;

	// Defaults from nvidia devblog
	static const EGLint configAttribs[] = {
		EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
		EGL_BLUE_SIZE, 8,
		EGL_GREEN_SIZE, 8,
		EGL_RED_SIZE, 8,
		EGL_DEPTH_SIZE, 8,
		EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
		EGL_NONE
	};
	EGLint requires[] = {
		EGL_RENDERABLE_TYPE,	EGL_OPENGL_BIT,
		EGL_SURFACE_TYPE,	EGL_PBUFFER_BIT,
		EGL_NONE };
	int nConfigs = 0;

	ok = eglGetConfigs(display, 0, 0, &nConfigs);
	std::cerr << nConfigs << " configs available." << std::endl;
	ok = eglChooseConfig(display, requires, 0, 0, &nConfigs);
	std::cerr << nConfigs << " matching configs available." << std::endl;
	ok = eglChooseConfig(display, requires, &config, 1, &nConfigs);
	DIEIFN(ok && nConfigs, "Cannot get config.")
	
	context = eglCreateContext(display, config, EGL_NO_CONTEXT, 0);
	DIEIFN(context != EGL_NO_CONTEXT, "Cannot create context");

	ok = eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, context);
	DIEIFN(ok, "Cannot bind context");

	std::cerr << "Api initialized :" << std::endl;
	printGLError();
	std::cout << glGetString(GL_VENDOR) << std::endl;
	printGLError();
	std::cerr << glGetString(GL_RENDERER) << std::endl;
	std::cerr << "OpenGL " << glGetString(GL_VERSION) << std::endl;
	std::cerr << "GLSL " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;

	
	std::cout << "Renderer initialized (EGL "<<major<<"."<<minor<<")." << std::endl;

}

Renderer::~Renderer()
{
	eglTerminate(display);
}

