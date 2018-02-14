
import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode

import drawingFuncWall


## create_box : partie ODE
def create_box(world, space, density, lx, ly, lz):
    """Create a box body and its corresponding geom."""

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setBox(density, lx, ly, lz)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "box"
    body.boxsize = (lx, ly, lz)

    # Create a box geom for collision detection
    geom = ode.GeomBox(space, lengths=body.boxsize)
    geom.setBody(body)

    return body, geom



# Create a world object
world = ode.World()
world.setGravity( (0,-9.81,0) )
world.setERP(0.8)
world.setCFM(1E-5)

# Create a space object
space = ode.Space()

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0,1,0), 0)

# A list with ODE bodies
bodies = []

# The geoms for each of the bodies
geoms = []

# A joint group for the contact joints that are generated whenever
# two bodies collide
contactgroup = ode.JointGroup()

## simulation loop
# Some variables used inside the simulation loop
fps = 50

dt = 1.0/fps
running = True
state = 0
counter = 0
objcount = 0
lasttime = time.time()


# keyboard callback
def _keyfunc (c, x, y):
    sys.exit (0)

glutKeyboardFunc (_keyfunc)

def soclefunc():
    global socle
    socle, geom2 = create_box(world,space, 10,echelle(1.),echelle(5.),echelle(5.))
    socle.setPosition( (0,0,0) )
    socle.setRotation([1., 0., 0,
                        0., 1., 0.,
                        0., 0., 1])
    return
prises = []
def prisefunc(posX, posY, posZ, tailleY, tailleZ, prof):
    prise, geomP = create_box(world, space, 10, echelle(prof),echelle(tailleY),echelle(tailleZ))
    prise.setPosition((posX,posY,posZ))
    socle.setRotation([1., 0., 0,
                        0., 1., 0.,
                        0., 0., 1])
    prises.append(prise)


## draw callback
def _drawfunc ():
    # Draw the scene
    prepare_GL()
    #for b in bodies:
        #draw_body(b)
    print("lksjds")
    soclefunc()
    draw_body(socle)
    glutSwapBuffers ()

glutDisplayFunc (_drawfunc)

# idle callback
def _idlefunc ():
    global counter, state, lasttime

    t = dt - (time.time() - lasttime)
    if (t > 0):
        time.sleep(t)

    # counter += 1
    # # State 1: Explosion and pulling back the objects
    # elif state==1:
    #     if counter==100:
    #         explosion()
    #     if counter>300:
    #         pull()
    #     if counter==500:
    #         counter=20

    #glutPostRedisplay ()

    # Simulate
    n = 2

    # for i in range(n):
    #     # Detect collisions and create contact joints
    #     space.collide((world,contactgroup), near_callback)

   ##       # Simulation step
    #     world.step(dt/n)

   ##       # Remove all contact joints
    #     contactgroup.empty()

   ##   lasttime = time.time()

glutIdleFunc (_idlefunc)

glutMainLoop ()