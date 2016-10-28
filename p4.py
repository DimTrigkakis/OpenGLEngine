import gate
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import pyaudio
import wave
import sys
from threading import Thread

def audio():
	chunk = 1024
	wf = wave.open("music.wav", 'rb')

	# create an audio object
	p = pyaudio.PyAudio()

	# open stream based on the wave object which has been input.
	stream = p.open(format =
		        p.get_format_from_width(wf.getsampwidth()),
		        channels = wf.getnchannels(),
		        rate = wf.getframerate(),
		        output = True)

	# read data (based on the chunk size)
	data = wf.readframes(chunk)

	# play stream (looping from beginning of file to the end)
	while data != '':
	    # writing to the stream is what *actually* plays the sound.
	    stream.write(data)
	    data = wf.readframes(chunk)

	# cleanup stuff.
	stream.close()    
	p.terminate()

t = Thread(target=audio, args=())
t.start()
myGate = gate.Gate()

l0,l1,l2,anim = 1,1,1,1
def right_click_event():
	myGate.camera.center = [0,0,myGate.camera.center[2]+30]
	print "right click event"
	return
def right_click_event_2():
	myGate.camera.center = [0,0,myGate.camera.center[2]-30]
	print "right click event"
	return

def light0(x,y):
	global l0
	l0 = 1-l0
	if l0 == 0:
		glDisable(GL_LIGHT0)
	else:
		glEnable(GL_LIGHT0)
def light1(x,y):
	global l1
	l1 = 1-l1
	if l1 == 0:
		glDisable(GL_LIGHT1)
	else:
		glEnable(GL_LIGHT1)
def light2(x,y):
	global l2
	l2 = 1-l2
	if l2 == 0:
		glDisable(GL_LIGHT2)
	else:
		glEnable(GL_LIGHT2)
def animation(x,y):
	global anim
	anim = 1-anim

cumulative = 0
def animate_f(timeval):
	
	timeval = 0.00001
	global anim
	if anim == 0:
		return
	myGate.camera.center[1] = 2
	global cumulative
	cumulative += timeval*6000
	go = myGate.gobject_list[5]
	go.location = (3+math.cos(cumulative),go.location[1],go.location[2])
	go = myGate.gobject_list[0]
	go.location = (3+5*math.cos(cumulative),go.location[1],go.location[2])
	
	return

def draw_object1(gid,tid,name):
	myGate.set_texture(tid)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [50/256.0, 20/256.0, 20/256.0, 1.0])
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1])
    	glMaterialfv(GL_FRONT, GL_SHININESS, [0.0])
	glMaterialfv(GL_BACK, GL_AMBIENT_AND_DIFFUSE, [50/256.0, 50/256.0, 50/256.0, 1.0])
	glShadeModel( GL_FLAT )
	glutSolidSphere(1,20,20)

def draw_object2(gid,tid,name):
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [20/256.0, 50/256.0, 20/256.0, 1.0])
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    	glMaterialfv(GL_FRONT, GL_SHININESS, [0.0])
	glMaterialfv(GL_BACK, GL_AMBIENT_AND_DIFFUSE, [50/256.0, 50/256.0, 50/256.0, 1.0])
	glShadeModel( GL_FLAT )
	glutSolidCube(1)
def draw_object3(gid,tid,name):
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [20/256.0, 20/256.0, 50/256.0, 1.0])
	glMaterialfv(GL_BACK, GL_AMBIENT_AND_DIFFUSE, [50/256.0, 50/256.0, 50/256.0, 1.0])
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    	glMaterialfv(GL_FRONT, GL_SHININESS, [100.0])
	glShadeModel( GL_SMOOTH )
	glutSolidTeapot(1)
def draw_object4(gid,tid,name):
	myGate.set_texture(tid)

	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [60/256.0, 60/256.0, 60/256.0, 1.0])
	glMaterialfv(GL_BACK, GL_AMBIENT_AND_DIFFUSE, [50/256.0, 50/256.0, 50/256.0, 1.0])
   	glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    	glMaterialfv(GL_FRONT, GL_SHININESS, [100.0])
	glShadeModel( GL_SMOOTH )
	glutSolidTeapot(1)

def draw_objecta(gid,tid,name):
	if l0 == 0:
		return
	glDisable(GL_LIGHTING)
	glColor3f(1,0,0,1)
	glutSolidSphere(0.1,20,20)
	glEnable(GL_LIGHTING)	
def draw_objectb(gid,tid,name):
	
	if l1 == 0:
		return
	glDisable(GL_LIGHTING)
	glColor3f(1,1,1,1)
	glutSolidSphere(0.1,20,20)
	glEnable(GL_LIGHTING)	
def draw_objectc(gid,tid,name):
	
	if l2 == 0:
		return
	glDisable(GL_LIGHTING)
	glColor3f(1,1,0,1)
	glutSolidSphere(0.1,20,20)
	glEnable(GL_LIGHTING)		

menu = [("zoom out",right_click_event),("zoom in",right_click_event_2)]
keys = [("Key",'0',light0),("Key",'1',light1),("Key",'2',light2),("Key",'f',animation)]
textures = ["earth.jpg","sun.jpg","mars.jpg","marble.jpg"]

myGate.add_gobject(draw_objecta)
myGate.add_gobject(draw_objectb)
myGate.add_gobject(draw_objectc)
myGate.add_gobject(draw_object1)
myGate.add_gobject(draw_object2)
myGate.add_gobject(draw_object3)
myGate.add_gobject(draw_object4,tid=3)
myGate.gobject_list[0].location = [3,3,0]
myGate.gobject_list[1].location = [0,1,0]
myGate.gobject_list[2].location = [0,0,3]
myGate.gobject_list[3].location = [-3,0,0]
myGate.gobject_list[4].location = [0,0,0]
myGate.gobject_list[5].location = [3,0,0]
myGate.gobject_list[6].location = [0,-5,0]
light0 = gate.Data(location=(0,0,0),type="Point",color=(1,0,0),parent=myGate.gobject_list[0])
light1 = gate.Data(location=(0,1,0),type="Spot",color=(1,1,1),parent=myGate.gobject_list[1])
light2 = gate.Data(location=(0,0,3),type="Point",color=(1,1,0),parent=myGate.gobject_list[2])
lights = [light0,light1,light2]
myGate.add_animate(animate_f)
myGate.foundation(menu,keys,textures,lights)


