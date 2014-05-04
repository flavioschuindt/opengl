from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
 
torus = None

class Torus:

	def __init__(self, inner_radius=0.5, outter_radius=1, sides=50, rings=50, x_rotated=0, y_rotated=0, z_rotated=0):

		self.inner_radius = inner_radius
		self.outter_radius = outter_radius
		self.sides = sides
		self.rings = rings
		self.x_rotated = x_rotated
		self.y_rotated = y_rotated
		self.z_rotated = z_rotated

	def rotate(self, x=0, y=0, z=0):
		self.x_rotated += x
		self.y_rotated += y
		self.z_rotated += z

	def reshape(self, x, y):
		if y == 0 or x == 0:
			return
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(40.0, x/y, 0.5, 20.0)

		glViewport(0, 0, x, y)

	def display(self):
		glMatrixMode(GL_MODELVIEW)
		# clear the drawing buffer.
		glClear(GL_COLOR_BUFFER_BIT)
		# clear the identity matrix.
		glLoadIdentity()
		# traslate the draw by z = -4.0
		# Note this when you decrease z like -8.0 the drawing will looks far , or smaller.
		glTranslatef(0.0, 0.0, -4.5)
		# Red color used to draw.
		glColor3f(0.8, 0.2, 0.1) 
		# changing in transformation matrix.
		# rotation about X axis
		glRotatef(self.x_rotated, 1.0, 0.0, 0.0)
		# rotation about Y axis
		glRotatef(self.y_rotated, 0.0, 1.0, 0.0)
		# rotation about Z axis
		glRotatef(self.z_rotated, 0.0, 0.0, 1.0)
		# scaling transfomation 
		glScalef(1.0, 1.0, 1.0)
		#built-in (glut library) function , draw you a Torus.

		glutSolidTorus(self.inner_radius, self.outter_radius, self.sides, self.rings)
		#Flush buffers to screen
		 
		glFlush()

		glutSwapBuffers()


def display():
	global torus
	torus.display()

def reshape(x, y):
	global torus
	torus.reshape(x, y)

def idle():
	global torus
	torus.rotate(y=1)
	display()

def main():
	global torus
	torus = Torus()
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(400, 350)
	glutCreateWindow("Torus")
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)
	glutMainLoop()
	return 0

if __name__  == '__main__': main()