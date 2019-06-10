import re

#m = re.match("def (.+?)\((.+?)\):", "def rightAngle(t,leafNum):")

#print m.group(1)
#print re.split(",",m.group(2))

#funcLine = "	return random.random()*78.506 + 56.933"
#phrase = "return"

#print re.search("return (.*)",funcLine).group(0)
#print re.search("return (.*)",funcLine).group(1)
#print re.search("return (.+?)",funcLine).group(2)


lpyFile = open("./fileText.py", 'r')

loop = True
seedString = []
meanString = []
stdString = []
returnString = []

while loop == True:
	funcLine = next(lpyFile)
	if funcLine[:1] != '#':
		returnMatch = re.search("return (.*)",funcLine)
		seedMatch = re.search("random.seed\((.+?)\)",funcLine)
		meanMatch = re.search("mean(.*)=(.*)",funcLine)
		stdMatch = re.search("std(.*)=(.*)",funcLine)

		if returnMatch != None:
			returnString = returnMatch.group(1) #use this to figure out the type of call - rand(seed), gauss(mean,std,seed), or poly(1,2,3,4,seed) - then format like M_polynomials
			loop = False
		elif seedMatch != None:
			seedString = seedMatch.group(1)
		elif meanMatch != None:
			#meanString = meanMatch.group(2)  ### old formatting results in extra whitespaces
			meanString = re.sub(r"\s+", "", meanMatch.group(2), flags=re.UNICODE)
		elif stdMatch != None:
			#stdString = stdMatch.group(2)  ### old formatting results in extra whitespaces
			stdString = re.sub(r"\s+", "", stdMatch.group(2), flags=re.UNICODE)

print "seeds are " + seedString
print "means are " + meanString
print "stds are " + stdString
print "returns are " + returnString