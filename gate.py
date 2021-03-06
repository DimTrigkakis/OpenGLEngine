from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time
import random
from math import *
from gobject import gObject
from PIL import Image
import pyaudio
import wave
import pygame

class Data(object):
	def __init__(self,**kwargs):
		self.__dict__.update(kwargs)

class Camera(object):
	center = None
	look = None
	up = None

WIDTH = 1280
HEIGHT = 960	

class Text(object):
	r = 1
	g = 1
	b = 1
	a = 1
	quote = "No quote available"
	def __init__(self):
		self.x = random.randint(150,300)
		self.y = random.randint(200,HEIGHT-200)

class Gate(object):

	stop = 0 # make this a high number for music to stop
	name = 'OGRE' # OpenGlRenderingEngine ~ OGRE
	fps = 60 
	HEIGHT = 0
	WIDTH = 0

	gobject_list = []
	colors = []

	Xrot, Yrot, Zrot, Scale, MINSCALE = [0,0,0,1., 0.01]

	menu_function_list = []
	keys_list = []
	animate_function = None
	camera = None

	gid = 0
	tids_true = []

	lights = []
	lid = 0

	def simple_print(self, x,  y,  font,  text_list):
	    global HEIGHT
	    glWindowPos2f(x,HEIGHT-y)
	    for text in text_list:
		    for ch in text :
			d = ord(ch)
		
			glutBitmapCharacter( GLUT_BITMAP_HELVETICA_12 , ctypes.c_int( d ) )

	def glut_print(self, x,  y,  font,  text_list):
	    global HEIGHT
	    glWindowPos2f(x,HEIGHT-y)
	    yt = 0
	    #glutBitmapString(GLUT_BITMAP_HELVETICA_12,text.encode('ascii'))
	    for text in text_list:
		    yt += 20
	    	    glWindowPos2f(x,HEIGHT-(y+yt))
		    for ch in text :
			d = ord(ch)
			if (d == 8217):
				d = 39
			if (d == 10):
				continue
			if (d < 0 or d > 128):
				continue
			#	(xx,yy) = glGetFloatv(GL_CURRENT_RASTER_POSITION)
			#    	#glWindowPos2f(xx,yy+10)
		    	#glWindowPos2f(xx,yy)
		
			glutBitmapCharacter( GLUT_BITMAP_HELVETICA_12 , ctypes.c_int( d ) )
		    	#glutStrokeCharacter(GLUT_STROKE_ROMAN, ctypes.c_int(ord(ch)))



	def window_init(self):
		global WIDTH, HEIGHT
		self.HEIGHT = HEIGHT
		self.WIDTH = WIDTH
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
		glutInitWindowSize(WIDTH,HEIGHT)
		glutInitWindowPosition(glutGet(GLUT_SCREEN_WIDTH)/2-WIDTH/2,glutGet(GLUT_SCREEN_HEIGHT)/2-HEIGHT/2)
		
		glutCreateWindow(self.name)
	
	def settings_init(self):
		
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_DEPTH_TEST)
	
	def light_init(self):
		glEnable(GL_LIGHTING)		
		glEnable( GL_NORMALIZE )

	def create_point_light(self,location=(0,0,0),color=(1.0,1.0,1.0),name= None,parent=None):
		x,y,z = location
		r,g,b = color
		lid = self.lid
		gobject = gObject()
		gobject.parent = parent
		gobject.name = name
		gobject.gid = self.gid
		self.gid += 1
		self.gobject_list.append(gobject)
		gobject.light=True
		gobject.lid = lid
		gobject.location = (x,y,z)
		lightPosition = [x,y,z,1.]
		lightColor = [r,g,b,1.0] 
		glLightfv(GL_LIGHT0+lid, GL_POSITION, lightPosition)
		glLightfv(GL_LIGHT0+lid, GL_DIFFUSE, lightColor)
		glLightfv(GL_LIGHT0+lid, GL_SPECULAR, lightColor)
		glLightf(GL_LIGHT0+lid, GL_CONSTANT_ATTENUATION,0.001)
		glLightf(GL_LIGHT0+lid, GL_LINEAR_ATTENUATION, 0.001)
		glLightf(GL_LIGHT0+lid, GL_QUADRATIC_ATTENUATION, 0.0001)
		glEnable(GL_LIGHT0+lid)
		self.lights.append(lid)
		self.lid += 1

	def find_gobject(self,name):
		for i in self.gobject_list:
			if i.name == name:
				return i

	def create_spot_light(self,location=(0,0,0),color=(1.0,0.0,1.0),name= None,parent=None):
		x,y,z = location
		r,g,b = color

		lid = self.lid
		gobject = gObject()
		gobject.parent = parent
		gobject.name = name
		gobject.gid = self.gid
		self.gid += 1
		self.gobject_list.append(gobject)
		gobject.light=True
		gobject.lid = lid
		gobject.location = (x,y,z)
		lightPosition = [x,y,z,1.]
		lightColor = [r,g,b,1.0] 
		glLightfv(GL_LIGHT0+lid, GL_POSITION, lightPosition)
		glLightfv(GL_LIGHT0+lid, GL_DIFFUSE, lightColor)
		glLightfv(GL_LIGHT0+lid, GL_SPECULAR, lightColor)
		glLightfv( GL_LIGHT0+lid, GL_SPOT_DIRECTION,  (0,-10,0) )
		glLightf(  GL_LIGHT0+lid, GL_SPOT_EXPONENT, 1 )
		glLightf(  GL_LIGHT0+lid, GL_SPOT_CUTOFF, 60.0 )
		glLightf(GL_LIGHT0+lid, GL_CONSTANT_ATTENUATION, 0.1)
		glLightf(GL_LIGHT0+lid, GL_LINEAR_ATTENUATION, 0.04)
		glLightf(GL_LIGHT0+lid, GL_QUADRATIC_ATTENUATION, 0)
		glEnable(GL_LIGHT0+lid)
		self.lights.append(lid)
		self.lid += 1

	def set_lights(self,lights):
		if lights == None:
			return
		for l in lights:
			if l.type == "Point":
				self.create_point_light(location=l.location,color=l.color,parent=l.parent)
				
			if l.type == "Spot":
				self.create_spot_light(location=l.location,color=l.color,parent=l.parent)


	def camera_init(self):
		self.camera = Camera()
		self.camera.center = [0,0,10]
		self.camera.look = [0,0,0]
		self.camera.up = [0,1,0]
		self.set_camera()

	def set_camera(self):
		global WIDTH, HEIGHT
		camera = self.camera
		glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
		gluPerspective(40.,WIDTH*1.0/HEIGHT,1.,4000.)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
		gluLookAt(camera.center[0],camera.center[1],camera.center[2],
                              camera.look[0],camera.look[1],camera.look[2],
                              camera.up[0],camera.up[1],camera.up[2])
		
                glRotatef( self.Yrot, 0., 1., 0. )
                glRotatef( self.Xrot, 1., 0., 0. )
		glRotatef( self.Zrot, 0., 0., 1. )
		glScalef(self.Scale,self.Scale,self.Scale)

	def set_menu(self,menu_function_list=None):
		if menu_function_list == None:
			return

		self.menu_function_list = list(menu_function_list)
		menu = glutCreateMenu(self.processMenuEvent)
		for i,x in enumerate(self.menu_function_list):
			glutAddMenuEntry(x[0],i)
	
	def processMenuEvent(self,event):
		self.menu_function_list[event][1]()
		return 0 # important		
	
	def random_colors(self):
		for i in range(100):
			self.colors.append((random.random(),random.random(),random.random()))

	def set_keys(self,keys):
		self.keys_list = keys
		glutKeyboardFunc(self.key_functions)
		glutKeyboardUpFunc(self.key_up_functions)
		glutMotionFunc(self.mouse_function)
		glutPassiveMotionFunc(self.mouse_function)
		glutMouseFunc(self.mouse_down_function)

	def mouse_function(self,x,y):
		for i in range(len(self.keys_list)):
			if self.keys_list[i][0] == "Mouse":
				self.keys_list[i][2](x,y)

	def mouse_down_function(self,button,state,x,y):
		for i in range(len(self.keys_list)):
			if self.keys_list[i][0] == "MouseLeft" and button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
				self.keys_list[i][2](x,y)
			if self.keys_list[i][0] == "MouseRight" and button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN:
				self.keys_list[i][2](x,y)
			if self.keys_list[i][0] == "MouseLeftUp" and button==GLUT_LEFT_BUTTON and state==GLUT_UP:
				self.keys_list[i][2](x,y)
			if self.keys_list[i][0] == "MouseRightUp" and button==GLUT_RIGHT_BUTTON and state==GLUT_UP:
				self.keys_list[i][2](x,y)
			if self.keys_list[i][0] == "MouseMiddle" and button==GLUT_MIDDLE_BUTTON and state==GLUT_DOWN:
				self.keys_list[i][2](x,y)
			
		return 0
	def key_functions(self,key,x,y):
		for i in range(len(self.keys_list)):
			if key == self.keys_list[i][1] and self.keys_list[i][0] == "Key":
				self.keys_list[i][2](x,y)
			
		return 0

	def key_up_functions(self,key,x,y):
		for i in range(len(self.keys_list)):
			if key == self.keys_list[i][1] and self.keys_list[i][0] == "KeyUp":
				self.keys_list[i][2](x,y)
		return 0
		
		
		
	def set_textures(self,textures):
		if textures == None:
			return 
		for t in textures:
			self.load_textures(t)

	def foundation(self,menu_function_list=None, keys=None,textures=None,gui=None,lights=None):
		self.window_init()
		self.light_init()
		self.settings_init()
		self.camera_init()
		self.random_colors()
		self.set_menu(menu_function_list)
		self.set_keys(keys)
		self.set_textures(textures)
		self.set_lights(lights)

		self.draw_text = None
		if (gui != None):
			self.draw_text = gui[0]

		glutDisplayFunc(self.display)
		glutIdleFunc(self.idle)            
		glutMainLoop()

		return

	def add_gobject(self,draw_function,tid=-1,parent=None,name=None,location=(0,0,0)):
		
		gobject = gObject()
		gobject.parent = parent
		gobject.name = name
		gobject.location = location
		gobject.gid = self.gid
		self.gid += 1
		gobject.tid = tid
		gobject.draw_function = draw_function
		self.gobject_list.append(gobject)
            	return
            

	def idle(self):	
	
		timemarkA = time.time()
		glutPostRedisplay()
		timemarkB = time.time()
		self.animate(timemarkB-timemarkA)

	def add_animate(self,f):
		self.animate_function = f		

	def animate(self,timeval):
		if self.animate_function != None:
			self.animate_function(timeval)
		return		         

	def display(self):

		self.set_camera()

		glClearColor(0.0, 0.0, 0.0, 0.0 )
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) 
		
		for go in self.gobject_list:
			go.draw()

		if (self.draw_text != None):
			self.draw_text()

		glutSwapBuffers()

		return

	def set_texture(self,tid):
		glBindTexture(GL_TEXTURE_2D, self.tids_true[tid])   
		
	def load_textures(self,path):
		image = Image.open(path)
		ix = image.size[0]
		iy = image.size[1]		
		try:
			image = image.tobytes("raw", "RGBX", 0, -1)
		except:
			image = Image.open("./template.jpg")
			ix = image.size[0]
			iy = image.size[1]	
			image = image.tobytes("raw", "RGBX", 0, -1)
		
		tid_true = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, tid_true)
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

		self.tids_true.append(tid_true)

	def draw_sphere(self,l1,l2): # texturing doesn't work
		for i in range(0, l1 + 1):
			lat0 = pi * (-0.5 + float(float(i - 1) / float(l1)))
			z0 = sin(lat0)
			zr0 = cos(lat0)

			lat1 = pi * (-0.5 + float(float(i) / float(l1)))
			z1 = sin(lat1)
			zr1 = cos(lat1)

			glShadeModel( GL_SMOOTH )
			glBegin(GL_QUAD_STRIP)

			for j in range(0, l2 + 1):
				lng = 2 * pi * float(float(j - 1) / float(l2))
				x = cos(lng)
				y = sin(lng)
				ss = (lng+0.628318530718)/(2*pi)
				tt0 = (lat0+1.88495559215)/(pi)
				tt1 = (lat1+1.88495559215)/(pi)
				ss = float("{0:.2f}".format(ss))
				tt0 = float("{0:.2f}".format(tt0))
				tt1 = float("{0:.2f}".format(tt1))
	                        glColor3f(1.0,1.0,1.0)
				glTexCoord2f(ss,tt0);
				glNormal3f(x * zr0, y * zr0, z0)
				glVertex3f(x * zr0, y * zr0, z0)
				
				glTexCoord2f(ss,tt1);
				glNormal3f(x * zr1, y * zr1, z1)
				glVertex3f(x * zr1, y * zr1, z1)

			glEnd()

	def decode(self,filename,decode_type="wireframe"):
		f = open("./"+filename,"r")
		t = f.read()

		vertex_entry = 0
		edge_entry = 0
		triangle_entry = 0
		ends = []
		index = 0
		
		lookup = "};"
		with open(filename) as myFile:
			for num, line in enumerate(myFile):
				if lookup in line:
					ends.append(num)
				if "struct point Helipoints[]" in line:	
					vertex_entry = num
				if "struct edge Heliedges[]" in line:
					edge_entry = num
				if "struct tri Helitris[]" in line:
					triangle_entry = num
				
		vertices = []
		edges = []
		triangles = []	
		if decode_type == "wireframe":
			triangles = None
			with open(filename) as myFile:
				for num, line in enumerate(myFile):
					if num <= vertex_entry:	
						continue
					if num >= ends[3]:
						break
					
					line = line.translate(None, '\n,{}f')
					line = line.lstrip()
					line = line.rstrip()
								
					a, b, c = line.split(" ")	
					vertices.append((float(a),float(b),float(c)))		
			with open(filename) as myFile:
                                for num, line in enumerate(myFile):
                                        if num <= edge_entry:
                                                continue
                                        if num >= ends[4]:
                                                break

                                        line = line.translate(None, '\n,{}f')
                                        line = line.lstrip()
                                        line = line.rstrip()

                                        a, b = line.split(" ")
                                        edges.append((float(a),float(b)))
		else:
                        edges = None
                        with open(filename) as myFile:
                                for num, line in enumerate(myFile):
                                        if num <= vertex_entry:
                                                continue
                                        if num >= ends[3]:
                                                break

                                        line = line.translate(None, '\n,{}f')
                                        line = line.lstrip()
                                        line = line.rstrip()

                                        a, b, c = line.split(" ")
                                        vertices.append((float(a),float(b),float(c)))
                        with open(filename) as myFile:
                                for num, line in enumerate(myFile):
                                        if num <= triangle_entry:
                                                continue
                                        if num >= ends[5]:
                                                break

                                        line = line.translate(None, '\n,{}f')
                                        line = line.lstrip()
                                        line = line.rstrip()
					line = ' '.join(line.split())
					a, b, c = line.split(" ")
                                        triangles.append((int(a),int(b),int(c)))

		return vertices,edges,triangles


	composition = 0
	def audio(self):
		while (self.stop > 0.0001):
			self.stop -= 0.0001
			continue
		chunk = 1024
		wf = None
		if (self.composition == 0):
			wf = wave.open("music.wav", 'rb')
		else:
			wf = wave.open("composition.wav", 'rb')
		self.composition = 1-self.composition

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
		    if self.stop > 0.0001:
			break
		    stream.write(data)
		    data = wf.readframes(chunk)

		# cleanup stuff.
		stream.close()    
		p.terminate()



