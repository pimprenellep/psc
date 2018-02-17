all : native.a

native.a : simulator.o climbermodel.o morphology.o
	ar rcs $@ $^

%.o : %.cpp
	g++ -c -fPIC -fwrapv ${CXXFLAGS} -fno-strict-aliasing -I/usr/include/python3.5 -o $@ $^
