import gate
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

myGate = gate.Gate()

# custom events
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

# custom animate
def animate_f(timeval):
	myGate.Yrot += 1
	return

# custom object
def draw_f2(gid,tid,name):
	myGate.set_texture(tid)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [256/256.0, 256/256.0, 256/256.0, 1.0])
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    	glMaterialfv(GL_FRONT, GL_SHININESS, [100.0])
	myGate.draw_sphere(20,20)
	return

# setting up menu, keys, textures
menu = [("zoom out",right_click_event),("zoom in",right_click_event_2)]
keys = [("Key",'a',a),("KeyUp",'b',bup)]
textures = ["earth.jpg","sun.jpg","mars.jpg"]

# adding the graphical objects and moving them
myGate.add_gobject(draw_f2,tid=0,name="Earth")
myGate.add_gobject(draw_f2,tid=1,parent=myGate.gobject_list[0],name="Sun")
myGate.add_gobject(draw_f2,tid=2,parent=myGate.gobject_list[1],name="Mars")
myGate.add_gobject(draw_f2,tid=-1,parent=myGate.gobject_list[2],name="SM")
myGate.gobject_list[0].location = [2,0,0]
myGate.gobject_list[1].location = [2,0,0]
myGate.gobject_list[2].location = [2,0,0]
myGate.gobject_list[3].location = [2,0,0]
myGate.add_animate(animate_f)

# final call for the main loop
myGate.foundation(menu,keys,textures)


