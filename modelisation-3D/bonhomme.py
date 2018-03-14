# pyODE example 3: Collision detection

# Originally by Matthias Baas.
# Updated by Pierre Gay to work without pygame or cgkit.

import sys, os, random, time, math, numpy
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode

# geometric utility functions
def scalp (vec, scal):
    vec[0] *= scal
    vec[1] *= scal
    vec[2] *= scal

def length (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

# prepare_GL
def prepare_GL():
    """Prepare drawing.
    """

    # Viewport
    glViewport(0,0,640,480)

    # Initialize
    glClearColor(0.8,0.8,0.9,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_FLAT)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective (45,1.3333,0.2,20)

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)

    # View transformation
    gluLookAt (2.4, 3.6, 4.8, 0.5, 0.5, 0, 0, 1, 0)

# draw_body : partie openGL
def draw_body(body):
    """Draw an ODE body.
    """

    x,y,z = body.getPosition() 
    R = body.getRotation()
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix()
    glMultMatrixd(rot) # on met rot au carré
    if body.shape=="box":
        sx,sy,sz = body.boxsize
        glScalef(sx, sy, sz)
        glutSolidCube(1)
    glPopMatrix()


# create_box : partie ODE
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




# Collision callback
def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.
    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """
    if (geom1.isfloor == 0 and geom2.isfloor == 0):
        return
    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())



######################################################################

# Initialize Glut
glutInit ([])

# Open a window
glutInitDisplayMode (GLUT_RGB | GLUT_DOUBLE)

x = 0
y = 0
width = 1280
height = 960
glutInitWindowPosition (x, y);
glutInitWindowSize (width, height);
glutCreateWindow (b"testode")

# Create a world object
world = ode.World()
world.setGravity( (0,-9.81,0) )
world.setERP(0.8)
world.setCFM(1E-5)

# Create a space object
space = ode.Space()

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0,1,0), 0)
floor.isfloor = 1;

# A joint group for the contact joints that are generated whenever
# two bodies collide
contactgroup = ode.JointGroup()

# Some variables used inside the simulation loop
fps = 50
dt = 1.0/fps
running = True
lasttime = time.time()


# keyboard callback
def _keyfunc (c, x, y):
    sys.exit (0)

glutKeyboardFunc (_keyfunc)

firstMouse = 1
lastX = 0
lastY = 0

#def mouse_callback (c, xpos, ypos):
#    global firstMouse, lastX, lastY
#    if(firstMouse):
#        lastX = xpos
#        lastY = ypos
#        firstMouse = 0
#
#    xoffset = xpos - lastX
#    yoffset = lastY - ypos
#    lastX = xpos
#    lastY = ypos
#
#    sensitivity = 0.05;
#    xoffset *= sensitivity
#    yoffset *= sensitivity
#
#    yaw   += xoffset
#    pitch += yoffset
#
#    if(pitch > 89.0):
#        pitch = 89.0
#    if(pitch < -89.0):
#        pitch = -89.0;
#
#    front.x = cos(yaw) * cos(pitch)
#    front.y = sin(pitch)
#    front.z = sin(yaw) * cos(pitch)
#    cameraFront = front
#
#glutMouseFunc( mouse_callback )
def brasfunc():
    global brasG, geom_brasG, brasL, geom_brasL
    brasG, geom_brasG = create_box(world,space, 1000, 0.5, 1, 0.5)
    geom_brasG.isfloor = 0
    brasG.setPosition( (-1,3.5,0) )
    brasG.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    
    brasL, geom_brasL = create_box(world,space, 1000, 0.5, 1, 0.5)
    geom_brasL.isfloor = 0
    brasL.setPosition( (1,3.5,0) )
    brasL.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])

def avantbrasfunc():
    global avantbrasG, geom_avantbrasG, avantbrasL, geom_avantbrasL
    avantbrasG, geom_avantbrasG = create_box(world,space, 1000, 0.5, 1, 0.5)
    geom_avantbrasG.isfloor = 0
    avantbrasG.setPosition( (-1,2.5,0) )
    avantbrasG.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    
    avantbrasL, geom_avantbrasL = create_box(world,space, 1000, 0.5, 1, 0.5)
    geom_avantbrasL.isfloor = 0
    avantbrasL.setPosition( (1,2.5,0) )
    avantbrasL.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])

def jambefunc():
    global jambeG, geom_jambeG, jambeL, geom_jambeL
    jambeG, geom_jambeG = create_box(world,space, 1000, 0.5,1,0.5)
    geom_jambeG.isfloor = 0
    jambeG.setPosition( (-0.5,0.5,0) )
    jambeG.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    
    jambeL, geom_jambeL = create_box(world,space, 1000, 0.5,1,0.5)
    geom_jambeL.isfloor = 0
    jambeL.setPosition( (0.5,0.5,0) )
    jambeL.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    return

def cuissefunc():
    global cuisseG, geom_cuisseG, cuisseL, geom_cuisseL
    cuisseG, geom_cuisseG = create_box(world,space, 1000, 0.5,1,0.5)
    geom_cuisseG.isfloor = 0
    cuisseG.setPosition( (-0.5,1.5,0) )
    cuisseG.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    
    cuisseL, geom_cuisseL = create_box(world,space, 1000, 0.5,1,0.5)
    geom_cuisseL.isfloor = 0
    cuisseL.setPosition( (0.5,1.5,0) )
    cuisseL.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    return

def troncfunc():
    global tronc, geom_tronc
    tronc, geom_tronc = create_box(world,space, 1000, 1.5,2,0.5)
    geom_tronc.isfloor = 0
    tronc.setPosition( (0,3,0) )
    tronc.setRotation([1, 0., 0, 0., 1., 0., 0., 0., 1])
    return

    

# draw callback
def _drawfunc ():
    # Draw the scene
    prepare_GL()
    print("lksjds")
    draw_body(jambeL)
    draw_body(jambeG)
    draw_body(cuisseL)
    draw_body(cuisseG)
    draw_body(tronc)
    draw_body(brasL)
    draw_body(brasG)
    draw_body(avantbrasL)
    draw_body(avantbrasG)
    glutSwapBuffers ()

troncfunc()
brasfunc()
jambefunc()
cuissefunc()
avantbrasfunc()

cuisseL_jambeL = ode.HingeJoint(world)
cuisseL_jambeL.attach(cuisseL, jambeL)
cuisseL_jambeL.setAnchor( (0.5,1,0) )
cuisseL_jambeL.setAxis( (1,0,0) )

cuisseG_jambeG = ode.HingeJoint(world)
cuisseG_jambeG.attach(cuisseG, jambeG)
cuisseG_jambeG.setAnchor( (-0.5,1,0) )
cuisseG_jambeG.setAxis( (1,0,0) )

tronc_cuisseG = ode.BallJoint(world)
tronc_cuisseG.attach(cuisseG, tronc)
tronc_cuisseG.setAnchor( (-0.5,2,0) )

tronc_cuisseL = ode.BallJoint(world)
tronc_cuisseL.attach(cuisseL, tronc)
tronc_cuisseL.setAnchor( (0.5,2,0) )

tronc_brasG = ode.BallJoint(world)
tronc_brasG.attach(brasG, tronc)
tronc_brasG.setAnchor( (-1,4,0) )

tronc_brasL = ode.BallJoint(world)
tronc_brasL.attach(brasL, tronc)
tronc_brasL.setAnchor( (1,4,0) )

brasL_avantbrasL = ode.HingeJoint(world)
brasL_avantbrasL.attach(avantbrasL, brasL)
brasL_avantbrasL.setAnchor( (1,3,0) )
brasL_avantbrasL.setAxis( (1,0,0) )

brasG_avantbrasG = ode.HingeJoint(world)
brasG_avantbrasG.attach(avantbrasG, brasG)
brasG_avantbrasG.setAnchor( (-1,3,0) )
brasG_avantbrasG.setAxis( (1,0,0) )

glutDisplayFunc (_drawfunc)

# idle callback
def _idlefunc ():
    global counter, state, lasttime

    t = dt - (time.time() - lasttime)
    if (t > 0):
        time.sleep(t)
        
    glutPostRedisplay ()

    # Simulate
    n = 2

    for i in range(n):
        # Detect collisions and create contact joints
        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()

    lasttime = time.time()

glutIdleFunc (_idlefunc)

glutMainLoop ()