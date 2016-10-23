from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class gObject(object):

	gid = 0
	name = None
	location = (0,0,0)
	rotation = (0,0,0)
	
	draw_function = None
	parent = None
	
	def transform(self):
		glTranslatef(self.location[0],self.location[1],self.location[2])
		glRotate(self.rotation[0],1,0,0)
		glRotate(self.rotation[1],0,1,0)
		glRotate(self.rotation[2],0,0,1)
		
	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()

		if self.parent != None:
			self.parent.transform()

		glTranslatef(self.location[0],self.location[1],self.location[2])
		glRotate(self.rotation[0],1,0,0)
		glRotate(self.rotation[1],0,1,0)
		glRotate(self.rotation[2],0,0,1)
		if self.draw_function != None:
			self.draw_function(self.gid,self.name)

		glPopMatrix()

		pass
