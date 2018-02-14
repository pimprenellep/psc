
# Originally by Matthias Baas.
# Updated by Pierre Gay to work without pygame or cgkit.

import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode
import drawingFuncWall as dfw
    


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


def soclefunc():
    global socle
    socle, geom2 = create_box(world,space, 10,dfw.echelle(1.),dfw.echelle(5.),dfw.echelle(5.))
    socle.setPosition( (0,0,0) )
    socle.setRotation([1., 0., 0,
                        0., 1., 0.,
                        0., 0., 1])
    return

prises = []

def prisefunc(posX, posY, posZ, tailleY, tailleZ, prof):
    prise, geomP = create_box(world, space, 10, dfw.echelle(prof),dfw.echelle(tailleY),dfw.echelle(tailleZ))
    prise.setPosition((posX,posY,posZ))
    socle.setRotation([1., 0., 0,
                        0., 1., 0.,
                        0., 0., 1])
    prises.append(prise)

