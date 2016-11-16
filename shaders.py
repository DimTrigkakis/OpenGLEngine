
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Create and Compile a shader
# but fail with a meaningful message if something goes wrong
program = None

def createAndCompileShader(type,source):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with 
    # an exception in case of syntax errors

    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader

def init():
	global program

	vertex_shader=createAndCompileShader(GL_VERTEX_SHADER,"""
	  
	uniform float waveTime;
	varying vec3 vTexCoord;

	void main(void)
	{

	//Get Multitexturing coords...
	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;


	//Move the water...
	gl_TexCoord[0].x += waveTime;
	gl_TexCoord[0].y += waveTime-2.0; //Make the water move direction vary a little.


	    // Normal in Eye Space
	    vec3 vEyeNormal = gl_NormalMatrix * gl_Normal;
	    // Vertex position in Eye Space
	    vec4 vVert4 = gl_ModelViewMatrix * gl_Vertex;
	    vec3 vEyeVertex = normalize(vVert4.xyz / vVert4.w);
	    vec4 vCoords = vec4(reflect(vEyeVertex, vEyeNormal), 0.0);
	    // Rotate by flipped camera
	    vCoords = gl_ModelViewMatrixInverse * vCoords;
	    vTexCoord.xyz = normalize(vCoords.xyz);
	    // Don't forget to transform the geometry!



	  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

	}

	""");

	fragment_shader=createAndCompileShader(GL_FRAGMENT_SHADER,"""
	
	uniform sampler2D waveTextureId;
	uniform sampler2D waveTextureIdRef;
	uniform float waveTime;
	varying vec3 vTexCoord;


	void main()
	{

	   vec4 color1 = texture2D(waveTextureId, vec2(gl_TexCoord[0]));
	   vec4 color2 = texture2D(waveTextureIdRef, vec2(vTexCoord));
	   

	   gl_FragColor = 0.6 * vec4(color1 + color2) * vec4(0.0, 1.0, 1.0, 0.50); 
	}
	""");

	# build shader program

	program=glCreateProgram()
	glAttachShader(program,vertex_shader)
	glAttachShader(program,fragment_shader)
	glLinkProgram(program)

	# try to activate/enable shader program
	# handle errors wisely
	return program

def enable():
	global program
	try:
	    glUseProgram(program)   
	except OpenGL.error.GLError:
	    print glGetProgramInfoLog(program)
	    raise

def disable():
	glUseProgram(0)
		
