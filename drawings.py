from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import numpy
from math import sqrt, cos, sin

name = 'Free Drawings'

current_h = 0
current_w = 0
has_clicked = False
indx = 0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Drawing:
    def __init__(self, points=[], color=(255, 0, 0)):
        self.points = points
        self.r, self.g, self.b = color
        self.matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    def add_point(self, x, y):
        p = Point(x=x, y=y)
        self.points.append(p)

    def translate(self, x, y, z=0):
        self.matrix[12] += x
        self.matrix[13] += y
        self.matrix[14] += z

    def rotate(self, teta, x, y, z):

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glRotatef(teta,x,y,z)
        modified_modelview = (GLfloat * 16)()
        modified_modelview =  glGetFloatv(GL_MODELVIEW_MATRIX).tolist()
        #import pdb
        #pdb.set_trace()
        self.matrix = [modified_modelview[i:i+4] for i in range(0, len(modified_modelview), 4)]
        glPopMatrix()

        '''# normalize vector

        norm = sqrt(x*x + y*y + z*z)

        x, y, z = (x/norm, y/norm, z/norm)

        c = cos(teta)
        s = sin(teta)

        rotate_matrix = numpy.matrix([
                                        [x*x*(1-c)+c, x*y*(1-c)-z*s, x*z*(1-c)+y*s, 0],
                                        [y*x*(1-c)+z*s, y*y*(1-c)+c, y*z*(1-c)-x*s, 0],
                                        [x*z*(1-c)-y*s, y*z*(1-c)+x*s, z*z*(1-c)+c, 0],
                                        [0, 0, 0, 1]
                                    ])

        current_modelview_matrix = [self.matrix[i:i+4] for i in range(0, len(self.matrix), 4)]

        self.matrix = numpy.matrix(
                                        current_modelview_matrix
                                    )

        res = numpy.dot(self.matrix, rotate_matrix).T.tolist()
        self.matrix = reduce(lambda x,y: x+y, res)'''

scene = []
current_drawing = None
picked_drawing = None
picked_drawing_point = None

MODE_DRAWING = 0
MODE_PICKING = 1
MODE_ROTATE = 2
mode = MODE_DRAWING

PICKING_WINDOW_W = 9
PICKING_WINDOW_H = 9

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(name)


    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(500)/float(500), 0.1, 10)

    glMatrixMode(GL_MODELVIEW)


    # Disable anti-aliasing

    glDisable (GL_BLEND)
    glDisable (GL_DITHER)
    glDisable (GL_FOG)
    glDisable (GL_LIGHTING)
    glDisable (GL_TEXTURE_1D)
    glDisable (GL_TEXTURE_2D)
    glDisable (GL_TEXTURE_3D)
    glShadeModel (GL_FLAT)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)
    glutMotionFunc(active_mouse_motion)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop()
    

def reshape(w, h):

    global current_h, current_w

    current_h = h
    current_w = w
    glViewport (0, 0, w, h) # Update viewport
    glMatrixMode (GL_PROJECTION) # Update projection
    glLoadIdentity() 
    gluOrtho2D(0.0, w, 0.0, h) # To map unit square to viewport => gluOrtho2D(0.0, 1.0, 0.0, 1.0) 
    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay() # request redisplay

def display():
    
    global scene
    glClearColor(0.5, 0.5, 0.5, 1.0) # Set background to gray
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear the window

    glLineWidth(2)

    for drawing in scene:
        glColor3ub(drawing.r, drawing.g, drawing.b)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glMultMatrixf(drawing.matrix)
        size_drawing = len(drawing.points)
        for i in range(size_drawing - 1):
            glBegin(GL_LINES)
            glVertex2f(drawing.points[i].x, drawing.points[i].y)
            glVertex2f(drawing.points[i+1].x, drawing.points[i+1].y)
            glEnd()

        glPopMatrix()
        glFlush()

    glutSwapBuffers() #Swap buffers

def mouse_motion(x, y):

    global has_clicked, current_drawing, current_h

    if mode == MODE_DRAWING:
        if has_clicked:
            current_drawing.add_point(x=x, y=current_h - y)
            glutPostRedisplay()

def active_mouse_motion(x, y):
    global picked_drawing, picked_drawing_point
    if mode == MODE_PICKING:
        if picked_drawing is not None:
            offset_x = x - picked_drawing_point.x
            offset_y = (current_h - y) - picked_drawing_point.y
            picked_drawing_point.x = x
            picked_drawing_point.y = current_h - y
            picked_drawing.translate(offset_x, offset_y)
            glutPostRedisplay()

def _get_next_color():
    global indx
    r = (indx & 0x000000FF) >>  0
    g = (indx & 0x0000FF00) >>  8
    b = (indx & 0x00FF0000) >> 16

    if r == 127 and g == 127 and b == 127:
        indx += 1
        r = indx & 0x000000FF >> 0
        g = indx & 0x0000FF00 >> 8
        b = indx & 0x00FF0000 >> 16

    indx += 1

    return (r, g, b)

def _pick(x, y, window_width, window_height):
    window_size = PICKING_WINDOW_W * PICKING_WINDOW_H
    array = (GLubyte * window_size)(0)
    array = glReadPixels(x, current_h - y, PICKING_WINDOW_W, PICKING_WINDOW_H, GL_RGB, GL_UNSIGNED_BYTE)

    array_length = len(array)
    for drawing in scene:
        for i in range(array_length-2):
            if chr(drawing.r) == array[i] and chr(drawing.g) == array[i+1] and chr(drawing.b) == array[i+2]:
                return drawing
            i += 3

    return None

        
def mouse_click(button, state, x, y):

    global has_clicked, indx, current_h, current_drawing, picked_drawing, picked_drawing_point
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if mode == MODE_DRAWING:

            if not has_clicked:

                has_clicked = True

                # Define drawing color
                color = _get_next_color()

                # First element of drawing
                current_drawing = Drawing(color=color, points=[])
                #current_drawing.points = []
                current_drawing.add_point(x=x, y=current_h - y)

                scene.append(current_drawing)

            else: # Second click, finishes the current drawing.

                has_clicked = False

                # Last element of drawing
                current_drawing.add_point(x=x, y=current_h - y)

                glutPostRedisplay()

        elif mode == MODE_PICKING:
            picked_drawing = _pick(x, y, PICKING_WINDOW_W, PICKING_WINDOW_H)
            if picked_drawing is not None:
                picked_drawing_point = Point(x=x, y=current_h - y)

        elif mode == MODE_ROTATE:
            picked_drawing.rotate(30, 0, 0, 1)
            glutPostRedisplay()


    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

        picked_drawing = _pick(x, y, PICKING_WINDOW_W, PICKING_WINDOW_H)

        if picked_drawing is not None:
            scene.remove(picked_drawing)

        glutPostRedisplay()

def keyboard(key, x, y):
    global mode, MODE_DRAWING, MODE_PICKING
    if key == 'd':
        mode = MODE_DRAWING
    elif key == 'p':
        mode = MODE_PICKING
    elif key == 'r':
        mode = MODE_ROTATE

if __name__ == '__main__': main()
