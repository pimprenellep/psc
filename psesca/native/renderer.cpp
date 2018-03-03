#include "renderer.hpp"

#include <iostream>
#include <cassert>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "shaders.hpp"

#define DIEIFN(ok, msg)		\
	if(!(ok)) {		\
		std::cerr << "Renderer : " msg << std::endl;	\
		printEGLError();				\
		printGLError();				\
		return;						\
	}


Renderer::Renderer(const Route *r) :
	route(r),
	width(1024),
	height(768),
	sampling(4),
	display(EGL_NO_DISPLAY),
	context(EGL_NO_CONTEXT),
	stripsFirst(0)
{
	initContext();
	if(context == EGL_NO_CONTEXT)
		return;

	std::cerr << "Api initialized :" << std::endl;
	std::cerr << glGetString(GL_VENDOR) << std::endl;
	std::cerr << glGetString(GL_RENDERER) << std::endl;
	std::cerr << "OpenGL " << glGetString(GL_VERSION) << std::endl;
	std::cerr << "GLSL " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;

	glEnable(GL_DEBUG_OUTPUT);

	
	GLenum status;

	glGenFramebuffers(1,&framebuffer);
	glGenFramebuffers(1, &rb_framebuffer);
	glGenRenderbuffers(1,&renderbuffer);
	glGenRenderbuffers(1,&depthbuffer);
	glGenRenderbuffers(1,&rb_renderbuffer);

	glBindFramebuffer(GL_DRAW_FRAMEBUFFER,framebuffer);

	glBindRenderbuffer(GL_RENDERBUFFER, renderbuffer);
	glRenderbufferStorageMultisample(GL_RENDERBUFFER, sampling, GL_RGBA, width, height);
	glFramebufferRenderbuffer(GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, renderbuffer);
	glBindRenderbuffer(GL_RENDERBUFFER, depthbuffer);
	glRenderbufferStorageMultisample(GL_RENDERBUFFER, sampling, GL_DEPTH_COMPONENT, width, height);
	glFramebufferRenderbuffer(GL_DRAW_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthbuffer);
	status = glCheckFramebufferStatus(GL_DRAW_FRAMEBUFFER);
	DIEIFN(status == GL_FRAMEBUFFER_COMPLETE, "Incomplete framebuffer.");

	glBindFramebuffer(GL_READ_FRAMEBUFFER, rb_framebuffer);

	glBindRenderbuffer(GL_RENDERBUFFER, rb_renderbuffer);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, width, height);
	glFramebufferRenderbuffer(GL_READ_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, rb_renderbuffer);
	status = glCheckFramebufferStatus(GL_READ_FRAMEBUFFER);
	DIEIFN(status == GL_FRAMEBUFFER_COMPLETE, "Incomplete readback framebuffer.");

	/*
	*/

	glViewport(0, 0, width, height);

	loadShaders();
	initProjection();
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_MULTISAMPLE);
	//glEnable(GL_BLEND);
	//glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	//glEnable(GL_POLYGON_SMOOTH);
	loadRoute();
	glClearColor(0.8, 0.8, 1.0, 1.0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	draw();
	saveToFile("out.ppm");
	printGLDebug();
	printGLError();
}

void Renderer::initContext()
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
	while(context == EGL_NO_CONTEXT && iConfig < nConfigs) {
		std::cerr << "Trying config " << iConfig << "..." << std::endl;
		context = eglCreateContext(display, configs[iConfig], EGL_NO_CONTEXT, 0);
		if(context == EGL_NO_CONTEXT){
			printEGLError();
		}
		iConfig++;

	}
	DIEIFN(context != EGL_NO_CONTEXT, "Cannot create context");
	delete[] configs;

	ok = eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, context);
	DIEIFN(ok, "Cannot bind context");

	std::cout << "Context initialized (EGL "<<major<<"."<<minor<<")." << std::endl;
}

void Renderer::loadShaders()
{
	const char *vertexShaderSource = Shaders::getVertexSource();
	const int vertexSourceLength = Shaders::getVertexSize();

	const char *fragmentShaderSource = Shaders::getFragmentSource();
	const int fragmentSourceLength = Shaders::getFragmentSize();

	vertexShader = glCreateShader(GL_VERTEX_SHADER);
	fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	program = glCreateProgram();
	GLint status = 0;

	glShaderSource(vertexShader, 1, &vertexShaderSource, &vertexSourceLength);
	glCompileShader(vertexShader);
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &status);
	if(!status) {
		GLint log_length = 1;
		glGetShaderiv(vertexShader, GL_INFO_LOG_LENGTH, &log_length);
		char * log = new char[log_length];
		log[0] = '\0';
		glGetShaderInfoLog(vertexShader, log_length, 0, log);
		std::cerr << "Cannot compile vertex shader :" << std::endl
			<< log;
		delete[] log;
	}

	glShaderSource(fragmentShader, 1, &fragmentShaderSource, &fragmentSourceLength);
	glCompileShader(fragmentShader);
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &status);
	if(!status) {
		GLint log_length = 1;
		glGetShaderiv(fragmentShader, GL_INFO_LOG_LENGTH, &log_length);
		char * log = new char[log_length];
		log[0]= '\0';
		glGetShaderInfoLog(fragmentShader, log_length, 0, log);
		std::cerr << "Cannot compile fragment shader :" << std::endl
			<< log;
		delete[] log;
	}

	glAttachShader(program, vertexShader);
	glBindAttribLocation(program, 0, "position");
	glBindAttribLocation(program, 1, "vNormal");
	glAttachShader(program, fragmentShader);
	glBindFragDataLocation(program, 0, "color");

	glLinkProgram(program);
	glGetProgramiv(program, GL_LINK_STATUS, &status);
	DIEIFN(status, "Cannot link shader.");
	glUseProgram(program);

	glm::vec3 light(1.0, 3.0, 2.0);
	light = glm::normalize(light);
	GLint loc = glGetUniformLocation(program, "light");
	glUniform4f(loc, light[0], light[1], light[2], 1.0 );
	glReleaseShaderCompiler();
}

void Renderer::initProjection()
{
	glm::vec3 t(0.0, 1.0, 2.0);
	glm::vec3 vz(1.0, 1.0, 0.0);
	vz -= t;
	glm::vec3 vy(0.0, 1.0, 0.0);
	glm::vec3 vx = glm::cross(vz, vy);

	float angle = glm::radians(90.0);
	float aspect = (float)width / height;
	float near = 0.1;

	vz = near * glm::normalize(vz);
	vx = near * (float)tan(angle / 2.0) * glm::normalize(vx);
	vy = near / aspect * (float)tan(angle / 2.0) * vy;

	glm::mat3x3 v(vx, vy, vz);
	v = glm::inverse(v);
	t = -v * t;
	glm::mat4x4 m(
			v[0][0], v[1][0], v[2][0], t[0],
			v[0][1], v[1][1], v[2][1], t[1],
			v[0][2], v[1][2], v[2][2], t[2] - 1.0,
			v[0][2], v[1][2], v[2][2], t[2]
		     );

	GLint loc = glGetUniformLocation(program, "projection");
	glUniformMatrix4fv(loc, 1, GL_TRUE, glm::value_ptr(m));
}

void Renderer::loadRoute()
{
	GLuint routeArray, routeBuffer, normalsBuffer;
	
	const int nHolds = route->getNHolds();
	const Hold *holds = route->getHolds();

	for(int i = 0; i < nHolds; i++) {
		glm::mat4 trans(
				1.0, 0.0, 0.0, 0.0,
				0.0, 1.0, 0.0, 0.0,
				0.0, 0.0, 1.0, 0.0,
				holds[i].x, holds[i].y, 0.0, 1.0
			       );
		holds[i].shape->getStrips(stripsComponents, stripsNormals, stripsIndexes, stripsCount, trans);
	}
	GLsizei bufSize = stripsComponents.size() * sizeof(stripsComponents[0]);

	glGenBuffers(1, &routeBuffer);
	glGenBuffers(1, &normalsBuffer);
	glGenVertexArrays(1, &routeArray);

	glBindVertexArray(routeArray);

	glBindBuffer(GL_ARRAY_BUFFER, routeBuffer);
	glBufferData(GL_ARRAY_BUFFER, 
			bufSize,
			&(stripsComponents[0]),
			GL_STATIC_DRAW);
	glBindVertexBuffer(0, routeBuffer, 0, 3 * sizeof(stripsComponents[0]));

	glBindBuffer(GL_ARRAY_BUFFER, normalsBuffer);
	glBufferData(GL_ARRAY_BUFFER, 
			bufSize,
			&(stripsNormals[0]),
			GL_STATIC_DRAW);
	glBindVertexBuffer(1, normalsBuffer, 0, 3 * sizeof(stripsNormals[0]));

	glVertexAttribFormat(0, 3, GL_FLOAT, GL_FALSE, 0);
	glVertexAttribBinding(0, 0);
	glEnableVertexAttribArray(0);

	glVertexAttribFormat(1, 3, GL_FLOAT, GL_FALSE, 0);
	glVertexAttribBinding(1, 1);
	glEnableVertexAttribArray(1);

	int nStrips = stripsCount.size();
	stripsFirst = new unsigned short* [nStrips];
	
	int cum = 0;
	stripsFirst[0] = &(stripsIndexes[0]);
	for(int i = 1; i < nStrips; i++) {
		cum += stripsCount[i-1];
		stripsFirst[i] = &(stripsIndexes[cum]);
	}
}

void Renderer::draw()
{
	glMultiDrawElements(GL_TRIANGLE_STRIP,
			&(stripsCount[0]),
			GL_UNSIGNED_SHORT,
 			(void**)stripsFirst,
			stripsCount.size());

	glFinish();
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
			delete[] msg;
			msg = new char[nextLength];
			length = nextLength;
		}
		glGetDebugMessageLog(1, length, 0, 0, 0, 0, 0, msg);
		std::cerr << msg << std::endl;
	}
	delete[] msg;
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

	glBindFramebuffer(GL_DRAW_FRAMEBUFFER,rb_framebuffer);
	glBindFramebuffer(GL_READ_FRAMEBUFFER,framebuffer);
	glBlitFramebuffer(0, 0, width, height, 0, 0, width, height, GL_COLOR_BUFFER_BIT, GL_NEAREST);
	glBindFramebuffer(GL_DRAW_FRAMEBUFFER,framebuffer);
	glBindFramebuffer(GL_READ_FRAMEBUFFER,rb_framebuffer);

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

	delete[] buf;
	stm.close();
	return false;
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

Renderer::~Renderer()
{
	delete[] stripsFirst;
	/*
	glFinish();
	glUseProgram(0);
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);
	glDeleteProgram(program);
	glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, 0);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, 0, 0);
	glBindRenderbuffer(GL_RENDERBUFFER, 0);
	glBindFramebuffer(GL_FRAMEBUFFER, 0);
	glDeleteRenderbuffers(1, &renderbuffer);
	glDeleteFramebuffers(1, &framebuffer);
	*/
	eglMakeCurrent(display, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
	eglDestroyContext(display, context);
	eglTerminate(display);
}

