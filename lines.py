from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'Lines'
elements = []
current_h = 0
current_w = 0

has_clicked = False
first_point_x = 0
first_point_y = 0
second_point_x = -1
second_point_y = -1

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(2000, 2000)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(name)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)
    
    glutMainLoop()
    return

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
    
    glClearColor(0.5, 0.5, 0.5, 1.0) # Set background to gray
    glClear(GL_COLOR_BUFFER_BIT) # Clear the window

    glLineWidth(2.5) 
    glColor3f(1.0, 0.0, 0.0)

    for element in elements:
        glBegin(GL_LINES)
        glVertex2f(element[0], element[1])
        glVertex2f(element[2], element[3])
        glEnd()

    glutSwapBuffers() #Swap buffers

    return

def mouse_motion(x, y):

    global has_clicked, first_point_x, first_point_y, second_point_x, second_point_y

    if has_clicked:

        second_point_x = x
        second_point_y = current_h - y # Convert GLUT coordinates to OpenGL coordinates

        if len(elements) == 0:
            elements.append((first_point_x, first_point_y, second_point_x, second_point_y))
        else:
            elements[-1] = (first_point_x, first_point_y, second_point_x, second_point_y)

        glutPostRedisplay()

        return

def mouse_click(button, state, x, y):

    global has_clicked, first_point_x, first_point_y, second_point_x, second_point_y, current_h
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if has_clicked == 0:

            has_clicked = True
            first_point_x = x
            first_point_y = current_h - y

        else:

            second_point_x = x
            second_point_y = current_h - y # Convert GLUT coordinates to OpenGL coordinates
            has_clicked = False

            # Draw the line

            elements.append((first_point_x, first_point_y, second_point_x, second_point_y))

            second_point_x = -1
            second_point_y = -1

            glutPostRedisplay()

if __name__ == '__main__': main()
