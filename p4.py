import gate
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

myGate = gate.Gate()

def right_click_event():
	myGate.camera.center = [0,0,myGate.camera.center[2]+30]
	print "right click event"
	return
def right_click_event_2():
	myGate.camera.center = [0,0,myGate.camera.center[2]-30]
	print "right click event"
	return


def a(x,y):
	print "a",x,y
	return

def bup(x,y):
	print "b up",x,y
	return

def animate_f(timeval):
	myGate.Yrot += 1
	return

def draw_f(gid,name):
	radius = 10
	width = 10
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [256/256.0, 256/256.0, 256/256.0, 1.0]);
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1]);
    	glMaterialfv(GL_FRONT, GL_SHININESS, [100.0]);
	myGate.gobject_list[gid].rotation = [45,0,0]
	glColor3f(1,0,0)
	glBegin(GL_TRIANGLES)
	glVertex2f( radius, width/2.0)
	glVertex2f(0,0)
	glVertex2f(radius,-width/2.0)
	glVertex2f(-radius,-width/2.0)
	glVertex2f(0,0)
	glVertex2f(-radius,width/2.0)
	glEnd()
	return 
def draw_f2(gid,name):
	#glEnable(GL_TEXTURE_2D)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [256/256.0, 256/256.0, 256/256.0, 1.0]);
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1]);
    	glMaterialfv(GL_FRONT, GL_SHININESS, [100.0]);
	myGate.gobject_list[gid].rotation = [0,90,0]
	myGate.draw_sphere(40,40)
	#glDisable(GL_TEXTURE_2D)

menu = [("zoom out",right_click_event),("zoom in",right_click_event_2)]
keys = [("Key",'a',a),("KeyUp",'b',bup)]
#textures = ["earth.jpg"]
textures = None

myGate.add_gobject(draw_f2,name="Earth")
myGate.add_gobject(draw_f)
myGate.add_animate(animate_f)
myGate.foundation(menu,keys,textures)


