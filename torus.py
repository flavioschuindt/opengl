from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import pi, cos, sin
 
scene = []

class Torus:

	def __init__(self, color, position, inner_radius=1, outter_radius=0.2, sides=50, rings=50, x_rotated=0, y_rotated=0, z_rotated=0):

		self.inner_radius = inner_radius
		self.outter_radius = outter_radius
		self.sides = sides
		self.rings = rings
		self.x_rotated = x_rotated
		self.y_rotated = y_rotated
		self.z_rotated = z_rotated
		self.color = color
		self.position = position
		self.points = []

	def rotate(self, x=0, y=0, z=0):
		self.x_rotated += x
		self.y_rotated += y
		self.z_rotated += z

	def calc_points(self):
		self.points = []
		two_pi = pi * 2
		a = self.outter_radius
		c = self.inner_radius + self.outter_radius
		for i in range(self.sides):
			for j in range(self.rings + 1):
				k = 1
				while k >= 0:
					s = (i + k) % self.sides + 0.5
					t = j % self.rings

					x = (c + a * cos(s * two_pi / self.sides)) * cos(t * two_pi / self.rings)
					y = (c + a * cos(s * two_pi / self.sides)) * sin(t * two_pi / self.rings) 
					z = a * sin(s * two_pi / self.sides)
					k -= 1
					self.points.append((x, y, z))

def display():
	global scene
	# clear the drawing buffer.
	glClear(GL_COLOR_BUFFER_BIT)
	for torus in scene:
		glMatrixMode(GL_MODELVIEW)
		# clear the identity matrix.
		glLoadIdentity()
		# traslate the draw by z = -4.0
		# Note this when you decrease z like -8.0 the drawing will looks far , or smaller.
		glTranslatef(*torus.position)

		glColor3f(*torus.color) 
		# changing in transformation matrix.
		# rotation about X axis
		glRotatef(torus.x_rotated, 1.0, 0.0, 0.0)
		# rotation about Y axis
		glRotatef(torus.y_rotated, 0.0, 1.0, 0.0)
		# rotation about Z axis
		glRotatef(torus.z_rotated, 0.0, 0.0, 1.0)

		points = torus.calc_points()

		glBegin(GL_QUAD_STRIP)
		for point in torus.points:
			glVertex3d(*point)
		glEnd()

		#Flush buffers to screen
		glFlush()

	glutSwapBuffers()

def reshape(x, y):
	if y == 0 or x == 0:
		return
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(40.0, x/y, 0.5, 20.0)

	glViewport(0, 0, x, y)
	glMatrixMode(GL_MODELVIEW)
	glutPostRedisplay()

def idle():
	for torus in scene:
		torus.rotate(y=10)
	display()

def main():
	global scene
	t1 = Torus(sides=4, rings=4000, color=(0,1,0), position=(1,0,-10))
	t2 = Torus(sides=4, rings=4000, color=(1,0,0), position=(-1,2,-10))

	scene.append(t1)
	scene.append(t2)

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(500, 500)
	glutInitWindowPosition(450, 200)
	glutCreateWindow("Torus")
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)
	glutMainLoop()
	return 0

if __name__  == '__main__': main()