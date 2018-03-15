Workflow
===

Python workflow
---
If you do not intend to modifiy the compiled part (controller, simulator, renderer), you do not need a full development setup. You will need :
* A git client : [git](https://git-scm.com/downloads), or [Github desktop](https://desktop.github.com/) for instance;
* The compiled runtime for your system : See **Dependencies/Runtime** below.
Then, a typical workflow cycle would be :
* **Git pull or rebase** to start working on the latest version;
* Edit and commit whatever you want;
* **Run the tests** from the /tests/ subdirectory and make sure you did not break anything;
* Push your modifications. If you trigger a merge or conflict, rerun the tests after resolving it. 

Full workflow
---
To modify the whole project, a more complete setup is needed. You will still need a git client. However, you should not use the precompiled runtime, instead, check **Dependencies/Development** and **Building on ...** below.

Windows users : after cloning the project on your machine, you should be able to open it as a **directory** from MS Visual Studio, and the CMake configuration should be detected. You can then generate the CMake cache and the project from the CMake menu. You will most likely need to adjust the CMake local configuration in order for MSVC to find the development libraries and headers. Then a typical workflow cycle would be :
* **Git pull or rebase** to start working on the latest version;
* Edit whatever you want;
* Generate the project to include your modifications ;
* **Run the tests** from the /tests/ subdirectory and make sure you did not break anything;
* Commit, test, and push your modifications. If you trigger a merge or conflict, rerun the tests after resolving it. 

Dependencies
====

_Bullets prefixed with_ Stratus _refer to Windows tools and libraries that can or should be found in the developer cloud._
_Using the [desktop sync client](https://nextcloud.com/install/#install-clients) is highly recommended for python developers._
 
Runtime
---
* Python3 
* _Stratus_ ODE shared runtime library
* _Stratus_ Compiled python modules and native library

Compiled modules should be installed in the directory containing the plain python modules (i.e. psesca/), or the directory containing them can be added to the [PYTHONPATH](https://docs.python.org/3.6/using/cmdline.html#envvar-PYTHONPATH).

Shared libraries must be made available to the system. For Windows (dll files), one can simply put them in the directory from which python is run, or the directory containing them can be added to the system PATH.

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
