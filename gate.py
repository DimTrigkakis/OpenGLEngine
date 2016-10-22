from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time

class Gate(object):
	name = 'OGRE'
	fps = 60 
	    
	def window_init(self):
            glutInit(sys.argv)
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
            glutInitWindowSize(800,800)
            glutInitWindowPosition(glutGet(GLUT_SCREEN_WIDTH)/2-400,glutGet(GLUT_SCREEN_HEIGHT)/2-400)
            glutCreateWindow(self.name)
	
	def light_init(self):
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            lightZeroPosition = [10.,4.,10.,1.]
            lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
            glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
            glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
            glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
            glEnable(GL_LIGHT0)
	def camera_init(self):
            glMatrixMode(GL_PROJECTION)
            gluPerspective(40.,1.,1.,40.)
            glMatrixMode(GL_MODELVIEW)
            gluLookAt(0,0,10,0,0,0,0,1,0)

	def foundation(self):
	    self.window_init()
            self.light_init()
	    self.camera_init()
            #glClearColor(0.,0.,0.,1.)
	    #glShadeModel(GL_SMOOTH)
	    #glEnable(GL_CULL_FACE)

            glutDisplayFunc(self.display)
	    glutIdleFunc(self.idle)            
	     
	    glutMainLoop()
	    return

	def idle(self):	
            timemarkA = time.time()
            glutPostRedisplay()
            timemarkB = time.time()
            self.animate(timemarkB-timemarkA)
        rot = 0
	def animate(self,timeval):
	    self.rot += self.fps*timeval
            print self.fps*timeval
            

	def display(self):
	    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	    #glPushMatrix()
	    
            color = [1.0,0.,0.,1.]
	    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
            glRotate3f(self.rot,1,0,0)
	    glutSolidSphere(2,20,20)
	    
	    #glPopMatrix()
	    glutSwapBuffers()
	    return


if __name__ == '__main__': 
	myGate = Gate()
	myGate.foundation()


