import random
import urllib2
import urllib

m = 1024*3
def heightmaps():
	#aesthetic_style()
	global m
	heightmap = [[0 for x in range(m)] for y in range(m)]
	for i in range(1,m):
		for j in range(1,m):
			average = (heightmap[i][j-1]+heightmap[i-1][j]+heightmap[i-1][j-1])/3.0
			heightmap[i][j] = (average*1.0012)+(random.random()-0.5)

	return heightmap

quotations = ""
def aesthetic_style():
	global quotations
	maxi = 10
	i = 0
	j = 0
	maxj = 10
	print "Downloading aesthetics"	
	while (j < maxj):
		response2 = urllib2.urlopen("https://en.wikiquote.org/wiki/Special:Random")
		site2 = response2.geturl()
		response2 = urllib2.urlopen(site2)
		html2 = response2.readlines()
		enable = False
		for line in html2:
			if "<p><b>" in line:
				enable = True
			if ('<li>' in line) and not ('<a' in line) and enable:		
				a = line.find('<li>')
				text = line[a+4:-1]
				text = text[0:text.find("<")]
				quotations+=text+"\n"
				j+= 1
				break
	f = open('quotations.txt','w')
	f.write(quotations)
	f.close()
	while (i < maxi):
		response = urllib2.urlopen("https://en.wikipedia.org/wiki/Special:Random")
		site = response.geturl()

		response = urllib2.urlopen(site)

		html = response.readlines()

	
		for line in html:
			if ('upload.wikimedia.org' in line) and ('.jpg' in line):		
				a = line.find('upload.wikimedia.org')
				line2 = line[a:-1]
				b = line2.find('.jpg"')
				endline = ".jpg"
				filename = line2[0:b+4]
				print filename, "FOUND"
				urllib.urlretrieve("https://"+filename, str(i)+".jpg")
				i+= 1
				break
		#print html
