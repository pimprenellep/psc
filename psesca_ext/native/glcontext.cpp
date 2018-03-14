#include "glcontext.hpp"

#include <iostream>
#include <assert.h>

#ifdef WITH_EGL

#define DIEIFN(ok, msg)		\
	if(!(ok)) {		\
		std::cerr << "Renderer : " msg << std::endl;	\
		printEGLError();				\
		return;						\
	}

GLContext::GLContext():
	display(EGL_NO_DISPLAY),
	context(EGL_NO_CONTEXT)
{
	EGLBoolean ok;

	std::cerr << eglQueryString(EGL_NO_DISPLAY, EGL_EXTENSIONS) << std::endl;

	EGLDeviceEXT devices[16];
	EGLint nDevices = 0;

	PFNEGLQUERYDEVICESEXTPROC eglQueryDevicesEXT =
		(PFNEGLQUERYDEVICESEXTPROC)eglGetProcAddress("eglQueryDevicesEXT");
	if (eglQueryDevicesEXT) {
		ok = eglQueryDevicesEXT(16, devices, &nDevices);
		DIEIFN(ok, "Cannot enumerate devices.");
	}

	std::cout << nDevices << " graphical devices found." << std::endl;


	PFNEGLGETPLATFORMDISPLAYEXTPROC eglGetPlatformDisplayEXT =
		(PFNEGLGETPLATFORMDISPLAYEXTPROC)eglGetProcAddress("eglGetPlatformDisplayEXT");
	assert(eglGetPlatformDisplayEXT);

	if (nDevices) {
		std::cout << "Devices found, trying to get device display." << std::endl;
		display = eglGetPlatformDisplayEXT(EGL_PLATFORM_DEVICE_EXT, EGL_DEFAULT_DISPLAY, 0);
	}
	else {
		std::cout << "No devices found, trying to get default display." << std::endl;
		display = eglGetDisplay(EGL_DEFAULT_DISPLAY);
	}
	if (display == EGL_NO_DISPLAY) {
		std::cerr << "Renderer : cannot get display." << std::endl;
		return;
	}

	EGLint major, minor;
	ok = eglInitialize(display, &major, &minor);
	if (!ok) {
		std::cerr << "Renderer : cannot initialize display." << std::endl;
		return;
	}

	std::cerr << eglQueryString(display, EGL_VENDOR) << std::endl;
	std::cerr << eglQueryString(display, EGL_CLIENT_APIS) << std::endl;
	std::cerr << eglQueryString(display, EGL_EXTENSIONS) << std::endl;

	EGLConfig *configs;
	EGLint requires[] = {
		EGL_RENDERABLE_TYPE,	EGL_OPENGL_BIT,
		EGL_SURFACE_TYPE,	0,
		EGL_NONE };
	int nConfigs = 0;

	ok = eglGetConfigs(display, 0, 0, &nConfigs);
	std::cerr << nConfigs << " configs available." << std::endl;
	ok = eglChooseConfig(display, requires, 0, 0, &nConfigs);
	std::cerr << nConfigs << " matching configs available." << std::endl;
	configs = new EGLConfig[nConfigs];
	ok = eglChooseConfig(display, requires, configs, nConfigs, &nConfigs);
	DIEIFN(ok && nConfigs, "Cannot get config.");

	ok = eglBindAPI(EGL_OPENGL_API);
	DIEIFN(ok, "Renderer : cannot bind api.");

	int iConfig = 0;
	while (context == EGL_NO_CONTEXT && iConfig < nConfigs) {
		std::cerr << "Trying config " << iConfig << "..." << std::endl;
		context = eglCreateContext(display, configs[iConfig], EGL_NO_CONTEXT, 0);
		if (context == EGL_NO_CONTEXT) {
			printEGLError();
		}
		iConfig++;

	}
	DIEIFN(context != EGL_NO_CONTEXT, "Cannot create context");
	delete[] configs;

	ok = eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, context);
	DIEIFN(ok, "Cannot bind context");

	std::cout << "Context initialized (EGL " << major << "." << minor << ")." << std::endl;
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

void GLContext::printEGLError() const
{
	EGLint err = eglGetError();

#define ERROR_CASE(E) \
	case E:		\
	std::cerr << "EGL error is " #E << std::endl; \
	break;

	switch (err) {
		ERRORS_EGL(ERROR_CASE)
	default:
		std::cerr << "Unknown EGL error : " << err << std::endl;
	}

#undef ERROR_CASE
}

GLContext::~GLContext()
{
	eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
	eglDestroyContext(display, context);
	eglTerminate(display);
}

#endif

#ifdef WITH_WGL
GLContext::GLContext()
{
	
}
GLContext::~GLContext()
{

}
#endif
