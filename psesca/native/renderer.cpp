#include "renderer.hpp"

#include <iostream>
#include <cassert>
#define EGL_EGLEXT_PROTOTYPES
#include <EGL/egl.h>
#include <EGL/eglext.h>

#define DIEIF(ok, msg)		\
	if(!ok) {		\
		std::cerr << "Renderer : " msg << std::endl;	\
		return;								\
	}

Renderer::Renderer()
{
	EGLBoolean ok;

	std::cerr << eglQueryString(EGL_NO_DISPLAY, EGL_EXTENSIONS) << std::endl;

	EGLDeviceEXT devices[16];
	EGLint nDevices = 0;

	PFNEGLQUERYDEVICESEXTPROC eglQueryDevicesEXT =
		(PFNEGLQUERYDEVICESEXTPROC) eglGetProcAddress("eglQueryDevicesEXT");
	if(eglQueryDevicesEXT) {
		ok = eglQueryDevicesEXT(16, devices, &nDevices);
		DIEIF(ok, "Cannot enumerate devices.");
	}

	std::cout << nDevices << " graphical devices found." << std::endl;


	PFNEGLGETPLATFORMDISPLAYEXTPROC eglGetPlatformDisplayEXT =
		(PFNEGLGETPLATFORMDISPLAYEXTPROC) eglGetProcAddress("eglGetPlatformDisplayEXT");
	assert(eglGetPlatformDisplayEXT);

	EGLDisplay dp;
	if(nDevices) {
		std::cout << "Devices found, trying to get device display." << std::endl;
		dp = eglGetPlatformDisplayEXT(EGL_PLATFORM_DEVICE_EXT, EGL_DEFAULT_DISPLAY, 0);
	} else {
		std::cout << "No devices found, trying to get mesa display." << std::endl;
		dp = eglGetPlatformDisplayEXT(EGL_PLATFORM_GBM_MESA, EGL_DEFAULT_DISPLAY, 0);
	}
	if(dp == EGL_NO_DISPLAY) {
		std::cerr << "Renderer : cannot get display." << std::endl;
		return;
	}

	EGLint major, minor;
	ok = eglInitialize(dp, &major, &minor);
	if(!ok) {
		std::cerr << "Renderer : cannot initialize display." << std::endl;
		return;
	}

	std::cerr << eglQueryString(dp, EGL_VENDOR) << std::endl;
	std::cerr << eglQueryString(dp, EGL_CLIENT_APIS) << std::endl;
	std::cerr << eglQueryString(dp, EGL_EXTENSIONS) << std::endl;

	ok = eglBindAPI(EGL_OPENGL_ES_API);
	DIEIF(ok, "Renderer : cannot bind api.")
	
	std::cout << "Renderer initialized (EGL "<<major<<"."<<minor<<")." << std::endl;

}

