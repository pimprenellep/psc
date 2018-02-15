from .shape import Shape
from numpy import array
from OpenGL.GL import glPushMatrix, glPopMatrix, glMultMatrixf
from OpenGL.GLUT import glutSolidCube

## Simple width-height-area description of a hold
class WHAShape(Shape):
    def __init__(self, width, height, area):
        self.width = width
        self.height = height
        self.area = area

    def glDraw(self, x, y):
        # Arbitrary depth
        depth = min(self.width, self.height)
        transfo = array((
                (self.width, 0.0, 0.0, 0.0),
                (0.0, self.height, 0.0, 0.0),
                (0.0, 0.0, depth, 0.0),
                (x, y, 0.5 * depth, 1.0)
                ))
        glPushMatrix()
        glMultMatrixf(transfo)
        glutSolidCube(1.0)
        glPopMatrix()

