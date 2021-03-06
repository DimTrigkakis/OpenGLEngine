
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Create and Compile a shader
# but fail with a meaningful message if something goes wrong
program = None
program2 = None
program3 = None
program4 = None

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
	global program, program2, program3

	vertex_shader=createAndCompileShader(GL_VERTEX_SHADER,"""
	  
	uniform float waveTime;
	varying vec3 vTexCoord;

	void main(void)
	{

	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;


	gl_TexCoord[0].x += waveTime;
	gl_TexCoord[0].y += waveTime-2.0; //Make the water move direction vary a little.


	    vec3 vEyeNormal = gl_NormalMatrix * gl_Normal;
	    vec4 vVert4 = gl_ModelViewMatrix * gl_Vertex;
	    vec3 vEyeVertex = normalize(vVert4.xyz / vVert4.w);
	    vec4 vCoords = vec4(reflect(vEyeVertex, vEyeNormal), 0.0);
	    vCoords = gl_ModelViewMatrixInverse * vCoords;
	    vTexCoord.xyz = normalize(vCoords.xyz);


	  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

	}

	""");
	vertex_shader_sphere=createAndCompileShader(GL_VERTEX_SHADER,"""
	  
	uniform float waveTime;
	varying vec3 vTexCoord;

	void main(void)
	{

	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;


	gl_TexCoord[0].x += waveTime;
	gl_TexCoord[0].y += waveTime-2.0; //Make the water move direction vary a little.


	    vec3 vEyeNormal = gl_NormalMatrix * gl_Normal;
	    vec4 vVert4 = gl_ModelViewMatrix * gl_Vertex;
	    vec3 vEyeVertex = normalize(vVert4.xyz / vVert4.w);
	    vec4 vCoords = vec4(reflect(vEyeVertex, vEyeNormal), 0.0);
	    vCoords = gl_ModelViewMatrixInverse * vCoords;
	    vTexCoord.xyz = normalize(vCoords.xyz);

	  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	  gl_Position[0] += (sin(gl_TexCoord[0].x)+cos(gl_TexCoord[0].y))*50.0;//*sin(waveTime*20.0)))*50.0;
	  gl_Position[1] += (sin(gl_TexCoord[1].x)+cos(gl_TexCoord[1].y))*50.0;//*cos(waveTime*20.0)))*50.0;

	}

	""");

	vertex_shader_nothing=createAndCompileShader(GL_VERTEX_SHADER,"""
	  
	uniform float waveTime;
	varying vec3 vTexCoord;

	void main(void)
	{

	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;



	    vec3 vEyeNormal = gl_NormalMatrix * gl_Normal;
	    vec4 vVert4 = gl_ModelViewMatrix * gl_Vertex;
	    vec3 vEyeVertex = normalize(vVert4.xyz / vVert4.w);
	    vec4 vCoords = vec4(reflect(vEyeVertex, vEyeNormal), 0.0);
	    vCoords = gl_ModelViewMatrixInverse * vCoords;
	    vTexCoord.xyz = normalize(vCoords.xyz);



	  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

	}

	""");

	fragment_shader_grass=createAndCompileShader(GL_FRAGMENT_SHADER,"""
	
	uniform sampler2D waveTextureId;
	uniform sampler2D waveTextureIdRef;
	uniform float waveTime;
	varying vec3 vTexCoord;


	void main()
	{

	   vec4 color1 = texture2D(waveTextureId, vec2(gl_TexCoord[0]));
	   vec4 color2 = texture2D(waveTextureIdRef, vec2(vTexCoord));
	   

	   gl_FragColor = 0.6 * vec4(color1 + color2) * vec4(0.1, 1.00, 1.0, 0.50); 
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
	   

	   gl_FragColor = 0.6 * vec4(color1 + color2) * vec4(0.1, 1.00, 1.0, 0.50); 
	}
	""");

	
	fragment_shader_snow=createAndCompileShader(GL_FRAGMENT_SHADER,"""


	#ifdef GL_ES
	precision highp float;
	#endif

	uniform float waveTime;
	uniform float vvv;

	//Util Start

	float PI=3.14159265;


	vec3 sim(vec3 p,float s){
	   vec3 ret=p;
	   ret=p+s/2.0;
	   ret=fract(ret/s)*s-s/2.0;
	   return ret;
	}

	vec2 rot(vec2 p,float r){
	   vec2 ret;
	   ret.x=p.x*cos(r)-p.y*sin(r);
	   ret.y=p.x*sin(r)+p.y*cos(r);
	   return ret;
	}

	vec2 rotsim(vec2 p,float s){
	   vec2 ret=p;
	   ret=rot(p,-PI/(s*2.0));
	   ret=rot(p,floor(atan(ret.x,ret.y)/PI*s)*(PI/s));
	   return ret;
	}

	float rnd(vec2 v){
	  return sin((sin(((v.y-1453.0)/(v.x+1229.0))*23232.124))*16283.223)*0.5+0.5; 
	}

	float noise(vec2 v){
	  vec2 v1=floor(v);
	  vec2 v2=smoothstep(0.0,1.0,fract(v));
	  float n00=rnd(v1);
	  float n01=rnd(v1+vec2(0,1));
	  float n10=rnd(v1+vec2(1,0));
	  float n11=rnd(v1+vec2(1,1));
	  return mix(mix(n00,n01,v2.y),mix(n10,n11,v2.y),v2.x);
	}

	//Util End

	 
	//Scene Start
	 

	//Snow
	float makeshowflake(vec3 p){
	  return length(p)-0.03;
	}

	float makeShow(vec3 p,float tx,float ty,float tz){
	  p.y=p.y+waveTime*tx;
	  p.x=p.x+waveTime*ty;
	  p.z=p.z+waveTime*tz;
	  p=sim(p,4.0);
	  return makeshowflake(p);
	}

	vec2 obj1(vec3 p){
	  float f=makeShow(p,1.11, 1.03, 1.38);
	  f=min(f,makeShow(p,1.72, 0.74, 1.06));
	  f=min(f,makeShow(p,1.93, 0.75, 1.35));
	  f=min(f,makeShow(p,1.54, 0.94, 1.72));
	  f=min(f,makeShow(p,1.35, 1.33, 1.13));
	  f=min(f,makeShow(p,1.55, 0.23, 1.16));
	  f=min(f,makeShow(p,1.25, 0.41, 1.04));
	  f=min(f,makeShow(p,1.49, 0.29, 1.31));
	  f=min(f,makeShow(p,1.31, 1.31, 1.13));  
	  return vec2(f,1.0);
	}
	 
	vec3 obj1_c(vec3 p){
	    return vec3(1,1,1);
	}


	vec3 obj2_c(vec3 p){
	  return vec3(1.0,0.5,0.2);
	}
	 
	//Objects union
	vec2 inObj(vec3 p){
	  return obj1(p);
	}
	 
	//Scene End
	 
	void main(void){
	  vec2 resolution = vec2(1000,1000);
	  vec2 vPos=-1.0+2.0*gl_FragCoord.xy/resolution.xy;
	 
	  //Camera animation
	  vec3 vuv=normalize(vec3(sin(waveTime)*0.5,1,2));
	  vec3 vrp=vec3(0,cos(waveTime*0.5)+2.5,0);
	  vec3 prp=vec3(sin(waveTime*0.5)*(sin(waveTime*0.39)*2.0+3.5),sin(waveTime*0.5)+3.5,cos(waveTime*0.5)*(cos(waveTime*0.45)*2.0+3.5));
	  float vpd=1.5;  
	 
	  //Camera setup
	  vec3 vpn=normalize(vrp-prp);
	  vec3 u=normalize(cross(vuv,vpn));
	  vec3 v=cross(vpn,u);
	  vec3 scrCoord=prp+vpn*vpd+vPos.x*u*resolution.x/resolution.y+vPos.y*v;
	  vec3 scp=normalize(scrCoord-prp);
	 
	  //lights are 2d, no raymarching
	  mat4 cm=mat4(
	    u.y,   u.y,   u.z,   -dot(u,prp),
	    v.x,   v.y,   v.z,   -dot(v,prp),
	    vpn.x, vpn.y, vpn.z, -dot(vpn,prp),
	    0.0,   0.0,   0.0,   1.0);
	 
	  vec4 pc=vec4(0,0,0,0);
	  const float maxl=80.0;
	  for(float i=0.0;i<maxl;i++){
	  vec4 pt=vec4(
	    sin(i*PI*2.0*7.0/maxl)*2.0*(1.0-i/maxl),
	    i/maxl*4.0,
	    cos(i*PI*2.0*7.0/maxl)*2.0*(1.0-i/maxl),
	    1.0);
	  pt=pt*cm;
	  vec2 xy=(pt/(-pt.z/vpd)).xy+vPos*vec2(resolution.x/resolution.y,1.0);
	  float c;
	  c=0.4/length(xy);
	  pc+=vec4(
		  (sin(i*5.0+waveTime*10.0)*0.5+0.5)*c,
		  (cos(i*3.0+waveTime*8.0)*0.5+0.5)*c,
		  (sin(i*1.0+waveTime*9.0)*0.5+0.5)*c,0.0);
	  }
	  pc=pc/maxl;
	  pc=smoothstep(0.0,1.0,pc);
	  pc=vec4(pc.x,pc.y,pc.z,1.0);
	  
	  //Raymarching
	  const vec3 e=vec3(0.1,0,0);
	  const float maxd=15.0; //Max depth
	 
	  vec2 s=vec2(0.9,0.0);
	  vec3 c,p,n;
	 
	  float f=1.0;
	  for(int i=0;i<5;i++){
	    if (abs(s.x)<.001||f>maxd) break;
	    f+=s.x;
	    p=prp+scp*f;
	    s=inObj(p);
	  }
	  
	  if (f<maxd){
	      c=obj1_c(p);
		c[0] += 0.5;
		c[1] += 0.5;
		gl_FragColor=vec4(c*max(1.0-f*.08,0.0),vvv);
	      
	  }
	  else gl_FragColor=vec4(0,0,0,vvv); //background color
	}


	""");

	program=glCreateProgram()
	glAttachShader(program,vertex_shader)
	glAttachShader(program,fragment_shader)
	glLinkProgram(program)
	program2=glCreateProgram()
	glAttachShader(program2,vertex_shader)
	glAttachShader(program2,fragment_shader_snow)
	glLinkProgram(program2)
	program3=glCreateProgram()
	glAttachShader(program3,vertex_shader_sphere)
	glAttachShader(program3,fragment_shader)
	glLinkProgram(program3)

	return program, program2,program3

def enable(select):
	try:
	    if (select == 1):
	    	glUseProgram(program)  
	    elif (select == 2):
	    	glUseProgram(program2)
	    else:
		glUseProgram(program3)
	    
	except OpenGL.error.GLError:
	    print glGetProgramInfoLog(program)
	    raise

def disable():
	glUseProgram(0)
		
