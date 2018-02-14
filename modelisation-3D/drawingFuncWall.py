
import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# geometric utility functions

def length (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)
    
def echelle(pixel):
    return (pixel*1)
    
    
## draw_body : partie openGL : attention appel à ODE car body est un objet ODE !! dessine des pavés
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


