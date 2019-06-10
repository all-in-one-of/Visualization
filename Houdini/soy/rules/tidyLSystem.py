# Converts clean L-System rules to Houdini-compliant L-System rules.

import os
import fileinput
import sys
import math
import re

readfile = sys.argv[1]
writefile = os.path.splitext(readfile)[0] + "_houdini.txt"

sourcefile = open(readfile, 'r')
destfile = open(writefile, 'w')

def parenSplit(s,iter):
     parts = []
     bracket_level = 0
     current = []
     rep = 0
     for c in (s):
         if c == ")" and bracket_level == 0 and rep<iter:
             parts.append("".join(current))
             current = []
             rep += 1
         else:
             if c == "(":
                 bracket_level += 1
             elif c == ")":
                 bracket_level -= 1
             current.append(c)
     parts.append("".join(current))
     return parts

ngauss = 4
seedoff = 100
seedincr = 100

for line in sourcefile:
	# pass comments through
	if line[:1] == '#':
		destfile.write(line)
	else:
		loopFlag = 0
		updateLine = line
		while loopFlag == 0:
			gaussSplit1 = updateLine.split('gauss(', 1)
			if len(gaussSplit1) > 1:
				#gaussSplit2 = gaussSplit1[1].split(')',1)
				gaussSplit2 = parenSplit(gaussSplit1[1],1)
				preGauss = gaussSplit1[0]
				gaussArgs = gaussSplit2[0]
				postGauss = gaussSplit2[1]
				# gauss(mean,std,seed)
				arg = gaussArgs.split(',')
				mean = arg[0]
				std = arg[1]
				seed = arg[2]

				### BEGIN STUART'S CODE
				offset = mean + "-" + str(0.5*ngauss)
				# the variance of a 0..1 uniform distribution is 1/12.
				# The variance of the sum of ngauss of those is ngauss/12, or std dev sqrt(ngauss/12).
				# Scale to suit.
	    
				scale = std + "/" + str(math.sqrt(ngauss/12.))
				terms = []
				for i in range(ngauss):
					terms.append( "rand(%s+%d)" % (seed, seedoff) )
					#terms.append( "rand(%s)" % (seed) )
					seedoff += seedincr
				repl = "%s+%s*(%s)" % (offset,scale, "+".join(terms)) 
				### END STUART'S CODE

				#newMiddle = "((rand("+arg[2]+")+rand("+arg[2]+"+1000)+rand("+arg[2]+"+2000)+rand("+arg[2]+"+3000)-2)*0.3333)*"+arg[1]+"+"+arg[0]
				updateLine = preGauss + repl + postGauss
			else:
				loopFlag = 1
		loopFlag = 0
		while loopFlag == 0:
			polySplit1 = updateLine.split('poly(', 1)
			if len(polySplit1) > 1:
				#polySplit2 = polySplit1[1].split(')',1)
				polySplit2 = parenSplit(polySplit1[1],1)
				prePoly = polySplit1[0]
				polyArgs = polySplit2[0]
				postPoly = polySplit2[1]
				# poly(Axxx,Bxx,Cx,D,seed)
				arg = polyArgs.split(',')
				newMiddle = arg[0]+"*"+arg[4]+"*"+arg[4]+"*"+arg[4]+"+"+arg[1]+"*"+arg[4]+"*"+arg[4]+"+"+arg[2]+"*"+arg[4]+"+"+arg[3]
				updateLine = prePoly + newMiddle + postPoly
			else:
				loopFlag = 1
		destfile.write(updateLine)
