import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode 
import climbingWall as cl



## prepare_GL
def prepare_GL():
    """Prepare drawing.
    """
    # Viewport
    glViewport(0,0,300,480) #x,y spécifie la position du coin gauche bas de la fenetre (en pixel), les deux chiffres suivants précisent la taille de l'image
    
    # Initialize
    glClearColor(0.8,0.8,0.9,0)# couleur de l'arrière plan
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
    gluLookAt (-10.0, 5.0, 3., 0., 0., 0, 0, 1, 0) #position of the eye point (3), position of the reference point (3), up vector (3)


# Initialize Glut
glutInit ([])

# Open a window
glutInitDisplayMode (GLUT_RGB | GLUT_DOUBLE)

x = 0
y = 0
width = 640
height = 480
glutInitWindowPosition (x, y);
glutInitWindowSize (width, height);
glutCreateWindow (b"testode")

## draw_body : partie openGL
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
    glMultMatrixd(rot) # on met rot au carré <- (etienne) heu... non.
    if body.shape=="box":
        sx,sy,sz = body.boxsize
        glScalef(sx, sy, sz)
        glutSolidCube(1)
    glPopMatrix()


## keyboard callback
def _keyfunc (c, x, y):
    sys.exit (0)

glutKeyboardFunc (_keyfunc)

## draw callback
def _drawfunc ():
    # Draw the scene
    print("dozpid")
    prepare_GL()
    #for b in bodies:
        #draw_body(b)
    cl.soclefunc()
    draw_body(cl.socle)
    cl.prisefunc(0.,0.,0.,1.,1.,2.)
    draw_body(cl.prises[0])
    print("draw")
    glutSwapBuffers ()
    
    
print("ici")
glutDisplayFunc (_drawfunc)




glutMainLoop ()
