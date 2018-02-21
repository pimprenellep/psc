from OpenGL.GLUT import glutInit

class Renderer:
    def __init__(self, route):
        self.route = route
        # GL initialization code
        glutInit()

    def draw(self):
        # Draw a frame in whatever the current context is
        self.drawRoute()
        pass

    def screenshot(self):
        # Render a single frame and save it as an image file.
        # Priviledged early testing method
        self.draw()
        print('Screenshot placeholder')


    def drawRoute(self):
        for hold in self.route.getHolds() :
            hold.shape.glDraw(hold.x, hold.y)

