import gate
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import sys
from threading import Thread
import generator
import numpy
import shaders

myGate = gate.Gate()

# Audio
t = Thread(target=myGate.audio, args=())
t.start()

# Init variables
character = [0,0]
forward_step = 0
backward_step = 0
right_step = 0
mouse_x = 0
mouse_y = 0
once = True
scale = 16
waveTime = 0.0
program = None
program2 = None
program3 = None
low = True
score = 0
score_max = 0
# Generator
heightmap, water_height = generator.heightmaps()

def Animate(timeval):
	
	global forward_step, right_step, backward_step,mouse_x,mouse_y, once,scale, waveTime, program, program2, program3, text, score_max

	# Time variable
	waveTime += 0.0001

	# Canvas creation update
	random_creation()
	
	# Shaders/Camera init
	if (once):
		once = False
		program, program2,program3 = shaders.init()	
		myGate.camera.center = [generator.m/2,30.0,generator.m/2]
		myGate.set_camera()

		return

	# Text alpha animation
	if (text != None):
		if text.a > 0:
			text.a -= 0.001
		text.x += 0.1

	# Canvas animation
	random_canvas = myGate.find_gobject("canvas")
	if (random_canvas != None):
		r = random_canvas.rotation
		random_canvas.rotation = (r[0],r[1]+waveTime*3,r[2])

	# Mouse rotation based on mouse x
	beta = 0
	if (mouse_x - myGate.WIDTH/2.0) > 200:
		beta = ((mouse_x - myGate.WIDTH/2.0)-200)/50.0
		right_step = 1
	elif (mouse_x - myGate.WIDTH/2.0) < -200:
		right_step = -1
		beta = ((-mouse_x + myGate.WIDTH/2.0)-200)/50.0

	# Adapt height of camera lookat based on mouse y
	myGate.camera.look[1] = myGate.camera.center[1] + ((myGate.HEIGHT-mouse_y)*20.0/myGate.HEIGHT - 15)
	
	# Sky, snow and player point light have to adapt to the y location
	(x,y,z) = myGate.camera.center
	l = myGate.find_gobject("player_point_light").location
	myGate.find_gobject("player_point_light").location = (0.99*l[0]+0.01*(x+5),0.9*l[1]+0.1*(y+10-8+math.cos(waveTime*400)),z)
	myGate.find_gobject("sky").location = (x+5,y,z)
	myGate.find_gobject("snow").location = (x+5,y,z)

	# Camera position and lookat based on heightmap and water height

	l = myGate.camera.look
	c = myGate.camera.center
	special = 0

	try:
		d1 = abs(heightmap[int(c[0])][int(c[2])]+2 - l[1])
		d2 = abs(heightmap[int(c[0])][int(c[2])]+2 - c[1])
		if d1 > 1:
			d1 = 1
		if d2 > 1: 
			d2 = 1
		if score < score_max:
			myGate.camera.look[1] = l[1]*0.9+0.1*(max(water_height+0.75,heightmap[int(c[0])][int(c[2])]+8))
			myGate.camera.center[1] = c[1]*0.9 + 0.1*(max(water_height+0.75,heightmap[int(c[0])][int(c[2])]+8))
		

	except:
	
		myGate.camera.look[1] = l[1]*0.9+0.1*(max(water_height+0.75,8))
		myGate.camera.center[1] = c[1]*0.9 + 0.1*(max(water_height+0.75,8))


	# Camera movement
	alpha = 0
	if forward_step:
		alpha = 0.08
	if backward_step:
		alpha = -0.08

	temp =  [c[0]+alpha*(l[0]-c[0]),c[1],c[2]+alpha*(l[2]-c[2])]
	if temp[0] > 0 and temp[2] > 0:
		myGate.camera.center = [c[0]+alpha*(l[0]-c[0]),c[1],c[2]+alpha*(l[2]-c[2])]
		myGate.camera.look = [l[0]+alpha*(l[0]-c[0]),l[1],l[2]+alpha*(l[2]-c[2])]
		if (score >= score_max):
			temp =  [c[0]+alpha*(l[0]-c[0]),c[1]+alpha*(l[1]-c[1]),c[2]+alpha*(l[2]-c[2])]
			myGate.camera.center = [c[0]+alpha*(l[0]-c[0]),c[1]+alpha*(l[1]-c[1]),c[2]+alpha*(l[2]-c[2])]
			myGate.camera.look = [l[0]+alpha*(l[0]-c[0]),l[1]+alpha*(l[1]-c[1]),l[2]+alpha*(l[2]-c[2])]
		
	r = 10
	if right_step != 0:
		alpha = -0.01*right_step*beta
		dy = c[2] - l[2]
		dx = l[0] - c[0]
		theta = numpy.arctan2(dy,dx)
		theta += alpha
		myGate.camera.look[0] = c[0]+r*math.cos(theta)
		myGate.camera.look[2] = c[2]-r*math.sin(theta)

	right_step = 0

def mouse_move(x,y):
	global mouse_x, mouse_y
	mouse_x = x
	mouse_y = y

def forward(x,y):
	global forward_step
	forward_step = 1
	return
def forward_stop(x,y):
	global mouse_x, mouse_y

	mouse_x = x
	mouse_y = y
	global forward_step
	forward_step = 0
	return
def backward(x,y):
	global backward_step
	backward_step = 1
	return
def backward_stop(x,y):
	global backward_step
	backward_step = 0
	return

def right_side(x,y):
	global right_step
	right_step = 1
	return
def right_side_stop(x,y):
	global right_step
	right_step = 0
	return
	
def left_side(x,y):
	global right_step
	right_step = -1
	return
def left_side_stop(x,y):
	global right_step
	right_step = 0
	return

def dist(center, (i,h,j)):
	x = center[0]
	y = center[1]
	z = center[2]

	return math.sqrt((i-x)*(i-x)+(j-z)*(j-z))

def draw_snow(gid,tid,name):

	if (low):
		return 
	if (once != True):
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)
		glEnable(GL_BLEND)
		glDisable(GL_DEPTH_TEST)
		shaders.enable(2)
		loc=glGetUniformLocation(program2,"waveTime")
		glUniform1f(loc,100*waveTime)
		loc2=glGetUniformLocation(program2,"vvv")
		glUniform1f(loc2,(math.cos(waveTime*30)-0.5)/2.0)

		glRotatef(waveTime,0,1,0)
		glutSolidSphere(200,10,10)
		glDisable(GL_BLEND)
		glEnable(GL_DEPTH_TEST)
		shaders.disable()	
	
def draw_water(gid,tid,name):
	global scale, water_height, program, program2, waveTime, once
	
	if (once != True):
		shaders.enable(1)
		loc=glGetUniformLocation(program,"waveTime")
		glUniform1f(loc,10*waveTime)

	draw_size =15
	if low:
		draw_size = 10

	myGate.set_texture(tid)
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [60/256.0, 60/256.0, 60/256.0, 1.0])
   	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0, 0, 0, 0])
    	glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0.0])
	glShadeModel( GL_SMOOTH )
	
	a1 = 3.0
	a2 = 30
	a3 = a2/1.0
	glBegin(GL_TRIANGLES)
	for ii in range(int(myGate.camera.center[0]/scale-draw_size),int(myGate.camera.center[0]/scale+draw_size)):
		i = scale*ii
		i1 = (i*a1 % a2)/a3
		i2 = ((i+scale)*a1 % a2)/a3
		for jj in range(int(myGate.camera.center[2]/scale-draw_size),int(myGate.camera.center[2]/scale+draw_size)):
			j = scale*jj
			j1 = (j*a1 % a2)/a3
			j2 = ((j+scale)*a1 % a2)/a3

			ifinal = i-myGate.camera.center[0]
			jfinal = j-myGate.camera.center[2]
			if (math.sqrt(ifinal**2+jfinal**2)) > draw_size*scale:
				continue

			if (i > 0 and j > 0 and i < generator.m-scale and j < generator.m-scale):
				
				glTexCoord2f(i1,j1)
				glVertex3f(i,water_height,j)
				glTexCoord2f(i2,j1)
				glVertex3f(i+scale,water_height,j)
				glTexCoord2f(i1,j2)
				glVertex3f(i,water_height,j+scale)

				glVertex3f(i,water_height,j+scale)
				glTexCoord2f(i2,j1)
				glVertex3f(i+scale,water_height,j)
				glTexCoord2f(i2,j2)
				glVertex3f(i+scale,water_height,j+scale)
	glEnd()
	shaders.disable()

def draw_heightmap(gid,tid,name):
	global scale,program3
	myGate.set_texture(tid)
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [60/256.0, 60/256.0, 60/256.0, 1.0])
   	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0, 0, 0, 0])
    	glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0.0])
	glShadeModel( GL_SMOOTH )


	draw_size =15
	if low:
		draw_size = 10

	glBegin(GL_TRIANGLES)
	glColor3f(0,1,0)
	glNormal3f(0,1,0)
	a1 = 3.0
	a2 = 30
	a3 = a2/1.0
	for ii in range(int(myGate.camera.center[0]/scale-draw_size),int(myGate.camera.center[0]/scale+draw_size)):
		i = scale*ii
		i1 = (i*a1 % a2)/a3
		i2 = ((i+scale)*a1 % a2)/a3
		for jj in range(int(myGate.camera.center[2]/scale-draw_size),int(myGate.camera.center[2]/scale+draw_size)):
				
			
			
			j = scale*jj
			j1 = (j*a1 % a2)/a3
			j2 = ((j+scale)*a1 % a2)/a3

			ifinal = i-myGate.camera.center[0]
			jfinal = j-myGate.camera.center[2]
			if (math.sqrt(ifinal**2+jfinal**2)) > draw_size*scale:
				continue
			
			if (i > 0 and j > 0 and i < generator.m-scale and j < generator.m-scale):
				glTexCoord2f(i1,j1)
				glVertex3f(i,heightmap[i][j],j)
				glTexCoord2f(i2,j1)
				glVertex3f(i+scale,heightmap[i+scale][j],j)
				glTexCoord2f(i1,j2)
				glVertex3f(i,heightmap[i][j+scale],j+scale)

				glVertex3f(i,heightmap[i][j+scale],j+scale)
				glTexCoord2f(i2,j1)
				glVertex3f(i+scale,heightmap[i+scale][j],j)
				glTexCoord2f(i2,j2)
				glVertex3f(i+scale,heightmap[i+scale][j+scale],j+scale)

	glEnd()



def draw_sky(gid,tid,name):
	
	global lights_on, program, program2, waveTime, once
	
	if (once != True):
		shaders.enable(1)
		loc=glGetUniformLocation(program,"waveTime")
		glUniform1f(loc,waveTime)

	#if  not lights_on:
	#	glDisable(GL_LIGHTING)

	myGate.set_texture(tid)
	glColor3f(0.6,0.6,0.6)
	if not lights_on:
		glScalef(220,220,220)
	else:
		glScalef(10,10,10)
	l1 = 20
	l2 = 20
	pi = math.pi
	for i in range(0, l1 + 1):
		lat0 = pi * (-0.5 + float(float(i - 1) / float(l1)))
		z0 = math.sin(lat0)
		zr0 = math.cos(lat0)

		lat1 = pi * (-0.5 + float(float(i) / float(l1)))
		z1 = math.sin(lat1)
		zr1 = math.cos(lat1)

		glBegin(GL_QUAD_STRIP)

		for j in range(0, l2 + 1):
			lng = 2 * pi * float(float(j - 1) / float(l2))
			x = math.cos(lng)
			y = math.sin(lng)
			ss = (lng+0.0628)/(6.22+0.0628)
			tt0 = (lat0+1.603)/(1.54+1.603)

			max_picture_radius = 0.5
			repeat = 10.0
			if lights_on:
				repeat = 1
			glTexCoord2f((repeat)*math.cos(2*pi*ss)*tt0/2+0.5,(repeat)*math.sin(2*pi*ss)*tt0/2+0.5);
			
			tt1 = (lat1+1.603)/(1.54+1.603)
			
			glVertex3f(x * zr0, y * zr0, z0)
			glTexCoord2f((repeat)*math.cos(2*pi*ss)*tt1/2+0.5,(repeat)*math.sin(2*pi*ss)*tt1/2+0.5);
			glVertex3f(x * zr1, y * zr1, z1)

		glEnd()
	glScalef(1,1,1)
	#if  not lights_on:
	#	glEnable(GL_LIGHTING)
	shaders.disable()

def draw_sphere(gid,tid,name):
	
	global lights_on
	if  not lights_on:
		glDisable(GL_LIGHTING)
	myGate.set_texture(tid)
	glColor3f(0.6,0.6,0.6)
	if not lights_on:
		glScalef(220,220,220)
	else:
		glScalef(10,10,10)
	l1 = 20
	l2 = 20
	pi = math.pi
	for i in range(0, l1 + 1):
		lat0 = pi * (-0.5 + float(float(i - 1) / float(l1)))
		z0 = math.sin(lat0)
		zr0 = math.cos(lat0)

		lat1 = pi * (-0.5 + float(float(i) / float(l1)))
		z1 = math.sin(lat1)
		zr1 = math.cos(lat1)

		glBegin(GL_QUAD_STRIP)

		for j in range(0, l2 + 1):
			lng = 2 * pi * float(float(j - 1) / float(l2))
			x = math.cos(lng)
			y = math.sin(lng)
			ss = (lng+0.0628)/(6.22+0.0628)
			tt0 = (lat0+1.603)/(1.54+1.603)

			max_picture_radius = 0.5
			repeat = 10.0
			if lights_on:
				repeat = 1
			glTexCoord2f((repeat)*math.cos(2*pi*ss)*tt0/2+0.5,(repeat)*math.sin(2*pi*ss)*tt0/2+0.5);
			
			tt1 = (lat1+1.603)/(1.54+1.603)
			
			glVertex3f(x * zr0, y * zr0, z0)
			glTexCoord2f((repeat)*math.cos(2*pi*ss)*tt1/2+0.5,(repeat)*math.sin(2*pi*ss)*tt1/2+0.5);
			glVertex3f(x * zr1, y * zr1, z1)

		glEnd()
	glScalef(1,1,1)
	if  not lights_on:
		glEnable(GL_LIGHTING)

def draw_object_node(gid,tid,name):
	glDisable(GL_LIGHTING)
	glColor3f(1,1,1,1)
	glutSolidSphere(0.1,20,20)
	glEnable(GL_LIGHTING)

lights_on = False
def draw_canvas(gid,tid,name):
	
	myGate.set_texture(tid)
	glColor3f(1,1,1)
	lights_on = True
	glDisable(GL_LIGHTING)
	glBegin(GL_TRIANGLE_STRIP)
	dwd = 1.001
	glTexCoord2f(0,0)
	glVertex3f(-4,-4,dwd)
	glTexCoord2f(0,1)
	glVertex3f(-4,4,dwd)
	glTexCoord2f(1,0)
	glVertex3f(4,-4,dwd)
	glTexCoord2f(1,1)
	glVertex3f(4,4,dwd)
	
	glEnd()
	glBegin(GL_TRIANGLE_STRIP)
	glTexCoord2f(0,0)
	glVertex3f(-4,-4,-dwd)
	glTexCoord2f(0,1)
	glVertex3f(-4,4,-dwd)
	glTexCoord2f(1,0)
	glVertex3f(4,-4,-dwd)
	glTexCoord2f(1,1)
	glVertex3f(4,4,-dwd)
	glEnd()
	glMatrixMode(GL_MODELVIEW)
	ss = 5.0
	dd = 1.0
	myGate.set_texture(3)
 	glBegin(GL_QUADS)
	glTexCoord2f(0,0)
        glVertex3f( ss, ss,-dd)
	glTexCoord2f(0,1)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss, ss, dd)
	glTexCoord2f(1,1)
        glVertex3f( ss, ss, dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss,-ss, dd)
	glTexCoord2f(0,1)
        glVertex3f(-ss,-ss, dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss,-ss,-dd)
	glTexCoord2f(1,1)
        glVertex3f( ss,-ss,-dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss, ss, dd)
	glTexCoord2f(0,1)
        glVertex3f(-ss, ss, dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss,-ss, dd)
	glTexCoord2f(1,1)
        glVertex3f( ss,-ss, dd)
 
	glTexCoord2f(0,0)
        glVertex3f( ss,-ss,-dd)
	glTexCoord2f(0,1)
        glVertex3f(-ss,-ss,-dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(1,1)
        glVertex3f( ss, ss,-dd)
 
	glTexCoord2f(0,0)
        glVertex3f(-ss, ss, dd) 
	glTexCoord2f(0,1)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss,-ss,-dd) 
	glTexCoord2f(1,1)
        glVertex3f(-ss,-ss, dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss, ss,-dd) 
	glTexCoord2f(0,1)
        glVertex3f( ss, ss, dd)
	glTexCoord2f(1,0)
        glVertex3f( ss,-ss, dd)
	glTexCoord2f(1,1)
        glVertex3f( ss,-ss,-dd)

        glEnd()

	glEnable(GL_LIGHTING)
		

text = None
import codecs
def quotation():
	f = codecs.open("quotations.txt",encoding='utf-8' ,mode="r")
	s = f.read()
	q = s.split("\n")
	r = random.choice(q)
	# process q
	A = -1
	B = 0
	ind = 0
	rquotes = []
	original = r
	for i in range(80):
		B = original[B:].find(" ")+ind
		if (B == -1):
			break
		if (random.random() > 0.85):
			
			if (original[A+1:B] != ""):
				rquotes.append(original[A+1:B])
			A = B
		B = B+1
		ind = B

	
	rquotes.append(original[A:])
	return rquotes

def draw_text():
	global text,score
	if (text != None and text.a > 0.1):
		blending = False 
		if glIsEnabled(GL_BLEND) :
			blending = True
		glEnable (GL_BLEND)
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		gluOrtho2D(0.0, 1.0, 0.0, 1.0)
		glMatrixMode(GL_MODELVIEW)
		glColor4f(text.r,text.g,text.b,text.a)
		myGate.glut_print( text.x , text.y , GLUT_BITMAP_9_BY_15 , text.quote )
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		if not blending :
			glDisable(GL_BLEND) 

	blending = False 
	if glIsEnabled(GL_BLEND) :
		blending = True
	glEnable (GL_BLEND)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0.0, 1.0, 0.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glColor4f(1,1,1,1)
	myGate.simple_print( 20 , 20 , GLUT_BITMAP_9_BY_15 , "score : "+str(score) + " / "+str(score_max) )
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	if not blending :
		glDisable(GL_BLEND) 
	
def change_music():
	# Audio
	myGate.stop = 50
	t = Thread(target=myGate.audio, args=())
	t.start()

def read_text(x,y):
	global random_canvas, text, random_jukebox, score
	

	if (random_canvas != None) and (dist(myGate.camera.center,(random_canvas.location[0],random_canvas.location[1],random_canvas.location[2])) < 50):
		if (random_canvas.once == True):
			text = gate.Text()
			text.quote = quotation()
			random_canvas.once = False
			score += 1
	if (random_jukebox != None) and (dist(myGate.camera.center,(random_jukebox.location[0],random_jukebox.location[1],random_jukebox.location[2])) < 50):	
		if (random_jukebox.once == True):
			random_jukebox.once = False
			change_music()
			score += 1
	if (random_geometry != None) and (dist(myGate.camera.center,(random_geometry.location[0],random_geometry.location[1],random_geometry.location[2])) < 50):	
		if (random_geometry.once == True):
			random_geometry.once = False
			score += 1
def draw_geometry(gid, tid, name):
	global shaders, waveTime, lights_on
	tid = 1
	myGate.set_texture(1)
	if (once != True):
		shaders.enable(3)
		loc=glGetUniformLocation(program,"waveTime")
		glUniform1f(loc,10*waveTime)
	glShadeModel( GL_SMOOTH )
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [60/256.0, 60/256.0, 60/256.0, 1.0])
   	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0, 0, 0, 0])
    	glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0.0])
	lights_on = True
	draw_sphere(gid,tid,name)
	lights_on = False
	glShadeModel( GL_FLAT )
	shaders.disable()
	return	

def draw_jukebox(gid,tid,name):
	myGate.set_texture(tid)
	glColor3f(1,1,1)
	glDisable(GL_LIGHTING)
	glMatrixMode(GL_MODELVIEW)
	ss = 5.0
	dd = 5.0
	myGate.set_texture(4)
 	glBegin(GL_QUADS)
	glTexCoord2f(0,0)
        glVertex3f( ss, ss,-dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(1,1)
        glVertex3f(-ss, ss, dd)
	glTexCoord2f(0,1)
        glVertex3f( ss, ss, dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss,-ss, dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss,-ss, dd)
	glTexCoord2f(1,1)
        glVertex3f(-ss,-ss,-dd)
	glTexCoord2f(0,1)
        glVertex3f( ss,-ss,-dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss, ss, dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss, ss, dd)
	glTexCoord2f(1,1)
        glVertex3f(-ss,-ss, dd)
	glTexCoord2f(0,1)
        glVertex3f( ss,-ss, dd)
 
	glTexCoord2f(0,0)
        glVertex3f( ss,-ss,-dd)
	glTexCoord2f(1,0)
        glVertex3f(-ss,-ss,-dd)
	glTexCoord2f(1,1)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(0,1)
        glVertex3f( ss, ss,-dd)
 
	glTexCoord2f(0,0)
        glVertex3f(-ss, ss, dd) 
	glTexCoord2f(1,0)
        glVertex3f(-ss, ss,-dd)
	glTexCoord2f(1,1)
        glVertex3f(-ss,-ss,-dd) 
	glTexCoord2f(0,1)
        glVertex3f(-ss,-ss, dd) 
 
	glTexCoord2f(0,0)
        glVertex3f( ss, ss,-dd) 
	glTexCoord2f(1,0)
        glVertex3f( ss, ss, dd)
	glTexCoord2f(1,1)
        glVertex3f( ss,-ss, dd)
	glTexCoord2f(0,1)
        glVertex3f( ss,-ss,-dd)

        glEnd()

	glEnable(GL_LIGHTING)   		

import random
random_canvas = None
random_jukebox = None
random_geometry = None
def random_creation():
	global random_canvas, random_jukebox, random_geometry



	if (random_canvas != None):
		x,y,z = random_canvas.location
		myGate.find_gobject("canvas_point").location = (x,y+10,z)

	if (random.random() < 0.01):
		rx,ry = 0,0
		while (abs(rx) < 100 or abs(ry) < 100):
			rx = +500*random.random()-250
			ry = +500*random.random()-250
		rz = 10
		rt = random.randint(0,10)+5
		if (random_canvas == None) or (dist(myGate.camera.center,(random_canvas.location[0],random_canvas.location[1],random_canvas.location[2])) > 250):
			
			if random_canvas != None:
				if len(myGate.gobject_list) != 0:
					myGate.gobject_list.remove(random_canvas)
				else:
					random_canvas = None
			
			myGate.add_gobject(draw_canvas,tid=rt,name="canvas",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			location=(myGate.camera.center[0],heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],myGate.camera.center[2])	
			random_canvas = myGate.find_gobject("canvas")
			random_canvas.once = True

		elif (random_canvas == None):
			myGate.add_gobject(draw_canvas,tid=rt,name="canvas",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			random_canvas = myGate.find_gobject("canvas")
			random_canvas.once = True

	if (random_jukebox != None):
		x,y,z = random_jukebox.location
		myGate.find_gobject("jukebox_point").location = (x,y+10,z)

	if (random.random() < 0.01):
		rx,ry = 0,0
		while (abs(rx) < 100 or abs(ry) < 100):
			rx = +500*random.random()-250
			ry = +500*random.random()-250
		rz = 10
		if (random_jukebox == None) or (dist(myGate.camera.center,(random_jukebox.location[0],random_jukebox.location[1],random_jukebox.location[2])) > 250):
			
			if random_jukebox != None:
				if len(myGate.gobject_list) != 0:
					myGate.gobject_list.remove(random_jukebox)
				else:
					random_jukebox = None
			
			myGate.add_gobject(draw_jukebox,tid=4,name="jukebox",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			location=(myGate.camera.center[0],heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],myGate.camera.center[2])	
			random_jukebox = myGate.find_gobject("jukebox")
			random_jukebox.once = True

		elif (random_jukebox == None):
			myGate.add_gobject(draw_jukebox,tid=4,name="jukebox",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			random_jukebox = myGate.find_gobject("jukebox")
			random_jukebox.once = True

	if (random_geometry != None):
		x,y,z = random_geometry.location
		myGate.find_gobject("geometry_point").location = (x,y+10,z)

	if (random.random() < 0.01):
		rx,ry = 0,0
		while (abs(rx) < 100 or abs(ry) < 100):
			rx = +500*random.random()-250
			ry = +500*random.random()-250
		rz = 10
		if (random_geometry == None) or (dist(myGate.camera.center,(random_geometry.location[0],random_geometry.location[1],random_geometry.location[2])) > 250):
			
			if random_geometry != None:
				if len(myGate.gobject_list) != 0:
					myGate.gobject_list.remove(random_geometry)
				else:
					random_geometry = None
			
			myGate.add_gobject(draw_geometry,tid=-1,name="geometry",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			location=(myGate.camera.center[0],heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],myGate.camera.center[2])	
			random_geometry = myGate.find_gobject("geometry")
			random_geometry.once = True

		elif (random_geometry == None):
			myGate.add_gobject(draw_geometry,tid=-1,name="geometry",location=(myGate.camera.center[0]+rx,rz+heightmap[int(myGate.camera.center[0])][int(myGate.camera.center[2])],ry+myGate.camera.center[2]))
			random_geometry = myGate.find_gobject("geometry")
			random_geometry.once = True
		
def none_call(gid,tid,name):
	pass

def create_entities():
	my_lights = []
	myGate.add_gobject(none_call,tid=-1,name="canvas_point",location=(0,10,0),parent=None)
	myGate.add_gobject(none_call,tid=-1,name="jukebox_point",location=(0,10,0),parent=None)
	myGate.add_gobject(none_call,tid=-1,name="geometry_point",location=(0,10,0),parent=None)
	my_lights.append( gate.Data(location=(0,15,0),type="Point",color=(0.9,1,0.9),parent=myGate.find_gobject("canvas_point")) )
	my_lights.append( gate.Data(location=(0,15,0),type="Point",color=(0.9,1,0.9),parent=myGate.find_gobject("jukebox_point")) )
	my_lights.append( gate.Data(location=(0,15,0),type="Point",color=(0.9,1,0.9),parent=myGate.find_gobject("geometry_point")) )
	return my_lights

menu = []
gui = [draw_text]
keys = [("Key",'w',forward),("KeyUp",'w',forward_stop),("Key",'d',right_side),("KeyUp",'d',right_side_stop),("Key",'s',backward),("KeyUp",'s',backward_stop),("Key",'a',left_side),("Key",'e',read_text),("KeyUp",'a',left_side_stop),("Mouse","None",mouse_move),("MouseLeft","None",forward),("MouseMiddle","None",read_text),("MouseRight","None",backward),("MouseLeftUp","None",forward_stop),("MouseRightUp","None",backward_stop)]
textures = ["grass.jpg","starnight.jpg","water.jpg","wood.jpg","jukebox.jpg"]

myGate.add_gobject(draw_object_node,name="player_point_light")
myGate.add_gobject(draw_heightmap,tid=0,name="heightmap")
myGate.add_gobject(draw_water,tid=2,name="water")
myGate.add_gobject(draw_sky,tid=1,name="sky")
myGate.add_gobject(draw_snow,tid=-1,name="snow")
light0 = gate.Data(location=(0,10,0),type="Point",color=(0.9,1,0.9),parent=myGate.find_gobject("player_point_light"))
lights = create_entities()

for t in range(10):
	textures.append(str(t)+".jpg")

myGate.add_animate(Animate)
true_lights = [light0]
for light in lights:
	true_lights.append(light)

myGate.foundation(menu,keys,textures,gui,true_lights)




