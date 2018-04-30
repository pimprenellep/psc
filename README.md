PSC : Analysing diffculty in climbing
===

Welcome on the repository of the INF/MEC02 team of the X2016 year group of the École polytechnique.

Build instructions can be found in the CONTRIBUTING guide.

Directory structure
---
/psesca/ is the main, pure python module
/psesca_ext/native is the native library handling low-level computation
/psesca_exet/psesca are the Cython extension classes (logically part of the psesca module) interfacing the former.

/tests/ contains executable python scripts which must be run from the tests directory

/doc/ contains general documentation and architecture

other directories are working directories with no releaseable content.
