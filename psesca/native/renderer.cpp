#include "renderer.hpp"

#include <iostream>
#include <cassert>


#define DIEIFN(ok, msg)		\
	if(!(ok)) {		\
		std::cerr << "Renderer : " msg << std::endl;	\
		printEGLError();				\
		printGLError();				\
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
	X(GL_INVALID_FRAMEBUFFER_OPERATION)	\
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

Renderer::Renderer(const Route *r) :
	route(r),
	width(1024),
	height(768),
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

	EGLConfig config;
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

	ok = eglBindAPI(EGL_OPENGL_API);
	DIEIFN(ok, "Renderer : cannot bind api.");
	
	context = eglCreateContext(display, config, EGL_NO_CONTEXT, 0);
	DIEIFN(context != EGL_NO_CONTEXT, "Cannot create context");

	ok = eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, context);
	DIEIFN(ok, "Cannot bind context");


	std::cerr << "Api initialized :" << std::endl;
	std::cerr << glGetString(GL_VENDOR) << std::endl;
	std::cerr << glGetString(GL_RENDERER) << std::endl;
	std::cerr << "OpenGL " << glGetString(GL_VERSION) << std::endl;
	std::cerr << "GLSL " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;

	glEnable(GL_DEBUG_OUTPUT);

	// straight from SO
	GLuint fbo, render_buf;
	glGenFramebuffers(1,&fbo);
	glGenRenderbuffers(1,&render_buf);
	glBindRenderbuffer(GL_RENDERBUFFER, render_buf);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, width, height);
	glBindFramebuffer(GL_FRAMEBUFFER,fbo);
	glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, render_buf);
	glBindFramebuffer(GL_FRAMEBUFFER,fbo);
	glViewport(0, 0, width, height);

	
	std::cout << "Renderer initialized (EGL "<<major<<"."<<minor<<")." << std::endl;

	loadShaders();
	loadRoute();
	glClearColor(1.0, 0.0, 0.0, 1.0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	draw();
	saveToFile("out.ppm");
	
}

void Renderer::loadShaders()
{
	const char *vertexShaderSource =
		"#version 130\n"
		//"layout(location = 0) in vec3 position;"
		"in vec4 position;"
		"void main()"
		"{"
		"	gl_Position = position - vec4(0.5, 0.5, 0.0, 0.0);"
		"}"
		;
	const int vertexSourceLength = strlen(vertexShaderSource);
	const char *fragmentShaderSource =
		"#version 130\n"
		"out vec4 color;"
		"void main()"
		"{"
		"	color = vec4( 0.0, 1.0, 0.0, 1.0 );"
		"}"
		;
	const int fragmentSourceLength = strlen(fragmentShaderSource);

	GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	GLuint program = glCreateProgram();
	GLint status;

	glShaderSource(vertexShader, 1, &vertexShaderSource, &vertexSourceLength);
	glCompileShader(vertexShader);
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &status);
	if(!status) {
		GLint log_length = 0;
		glGetShaderiv(vertexShader, GL_INFO_LOG_LENGTH, &log_length);
		char * log = new char[log_length];
		glGetShaderInfoLog(vertexShader, log_length, 0, log);
		std::cerr << "Cannot compile vertex shader :" << std::endl
			<< log;
	}

	glShaderSource(fragmentShader, 1, &fragmentShaderSource, &fragmentSourceLength);
	glCompileShader(fragmentShader);
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &status);
	if(!status) {
		GLint log_length = 0;
		glGetShaderiv(fragmentShader, GL_INFO_LOG_LENGTH, &log_length);
		char * log = new char[log_length];
		glGetShaderInfoLog(fragmentShader, log_length, 0, log);
		std::cerr << "Cannot compile fragment shader :" << std::endl
			<< log;
	}

	glAttachShader(program, vertexShader);
	glBindAttribLocation(program, 0, "position");
	glAttachShader(program, fragmentShader);
	glBindFragDataLocation(program, 0, "color");

	glLinkProgram(program);
	glGetProgramiv(program, GL_LINK_STATUS, &status);
	DIEIFN(status, "Cannot link shader.");
	glUseProgram(program);
	printGLError();

}

void Renderer::loadRoute()
{
	GLuint routeArray, routeBuffer;
	GLfloat sq[] = {
		0.0, 0.0, 0.0, 
		1.0, 0.0, 0.0,
		0.0, 1.0, 0.0,
		1.0, 1.0, 0.0
	};
	glGenBuffers(1, &routeBuffer);
	glGenVertexArrays(1, &routeArray);

	glBindBuffer(GL_ARRAY_BUFFER, routeBuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(sq), sq, GL_STATIC_DRAW);

	glBindVertexArray(routeArray);
	glBindVertexBuffer(0, routeBuffer, 0, 3 * sizeof(*sq));
	glVertexAttribFormat(0, 3, GL_FLOAT, GL_FALSE, 0);
	glVertexAttribBinding(0, 0);
	glEnableVertexAttribArray(0);

}

void Renderer::draw()
{
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
	glFinish();
	printGLDebug();
	printGLError();
}

void Renderer::printGLDebug()
{
	int nMessages = 0;
	char *msg = 0;
	int length = 0;
	int nextLength;

	glGetIntegerv(GL_DEBUG_LOGGED_MESSAGES, &nMessages);
	for(int i = 0; i < nMessages; i++) {
		glGetIntegerv(GL_DEBUG_NEXT_LOGGED_MESSAGE_LENGTH, &nextLength);
		if(nextLength > length) {
			delete msg;
			msg = new char[nextLength];
			length = nextLength;
		}
		glGetDebugMessageLog(1, length, 0, 0, 0, 0, 0, msg);
		std::cerr << msg << std::endl;
	}
	delete msg;
}

bool Renderer::saveToFile(const char *file)
{
	std::ofstream stm(file, std::ios_base::trunc | std::ios_base::binary);

	if(!stm) {
		std::cerr << "Cannot open file " << file << "." << std::endl;
		return true;
	}


	unsigned char *buf = new unsigned char[width * height * 4];

	for(unsigned char *p = buf; p != buf + 4*width*height; p++) *p = 255;

	glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, buf);

	stm << "P6\n"<<width<<'\n'<<height<<"\n255\n";
	unsigned char *p = buf + 4*width*(height-1);
	for(int i = 0; i < height; i++) {
		for(int j = 0; j < width; j++) {
			stm << (unsigned char)*(p++);
			stm << (unsigned char)*(p++);
			stm << (unsigned char)*(p++);
			p++;
		}
		p -= 2*4*width;
	}

	delete buf;
	stm.close();
	return false;
}

Renderer::~Renderer()
{
	eglTerminate(display);
}

