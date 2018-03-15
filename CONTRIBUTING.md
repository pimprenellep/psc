Dependencies
====

_Bullets prefixed with_ Stratus _refers to tools and libraries that can or should be found in the developper cloud_
 
Runtime
---
* Python3 
* _Stratus_ ODE shared runtime library
* _Stratus_ Compiled python modules and native library
Compiled modules should be installed in the directory containing the plain pyhon modules (i.e. psesca/)
Shared libraries must be made available to the system. 
For Windows (dll files), one can simply put them in the directory frow which python is run.

Development
---
* Python3 with setuptools and cython
* CMake
* C++ compiler (gcc or msvc)
* ODE development libraries
* GLM header-only library
* Platform-specific OpenGL libraries

Building on GNUL/Linux
===
Rendering requires a working EGL setup.
CMake should work just fine with distribution-provided packages

Building on Windows
===
Required/recommended tools :
* [Python3](https://www.python.org/windows/) or larger Python3 distribution (e.g. Anaconda)
* [Cython](http://docs.cython.org/en/latest/src/quickstart/install.html) can be installed in Python from pip if not already provided
* Prefered compiler is Microsoft's [Visual Studio](https://www.visualstudio.com/vs/), including if not already installed :
  * _Windows development with c++_ workload
  * CMake
  * Github client
* _Stratus_ [GLM header files](https://github.com/g-truc/glm/releases/)
* _Stratus_ [ODE](https://bitbucket.org/odedevs/ode/downloads/) library compiled with single-precision as a shared library
