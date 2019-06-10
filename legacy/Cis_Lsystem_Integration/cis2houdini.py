# All we need is to translate L-Py code into Houdini. There's no need to have two separate scripts.
# The L-Py code might need a comment line that indicates where the FUNCTIONS begin and end and where the RULES begin and end, though.

# LPY File must be of the form:
# 
# totalPlants = 500
# percentDeviation = 0.1
#
# # CIS_BEGIN_FUNCTIONS
#
# # CIS_BEGIN_RULES
#
# production:
#
# endlsystem



#! /usr/bin/env python

import os
import sys
import re
import math

infname = sys.argv[1]
outfname = os.path.splitext(infname)[0] + "_houdini.txt"

print >>sys.stderr, "Processing %s into %s" % (infname, outfname)


myfuncs = re.compile( r'(gauss|uniform|poly4)\(([^()]+)*\)' )

#These are Stuart's hard-coded metas for Houdini
seedvar = "t"

ngauss = 4

seedoff = 100
seedincr = 100


def getMetas(lpyFile):

	metas = dict()
	line = ""
	endMetas = None

	while endMetas == None:
		tp = re.search("(.*)totalPlants(.*)=(.*)",line)
		if tp != None:
			metas["totalPlants"] = tp.group(3)
		pd = re.search("(.*)percentDeviation(.*)=(.*)",line)
		if pd != None:
			metas["percentDeviation"] = pd.group(3)
		# for instance, "percentDev"
		line = lpyFile.next()
		endMetas = re.search("(.*)#CIS_BEGIN_FUNCTIONS(.*)",line)
	return metas


def polynomialString(returnString, meanString, stdString, seedString, metas):

	gauss = re.search("(.*)random.gauss\((.*)\)(.*)",returnString)
	uniform = None; #TODO
	poly = None; #TODO
	random = re.search("(.*)random.random\(\)(.*)",returnString)

	seedStringEdited = seedString
	stdStringEdited = stdString

	if seedString != []:
		seedStringEdited = re.sub("plantId", "b", seedStringEdited)
		seedStringEdited = re.sub("totalPlants", str(metas["totalPlants"]), seedStringEdited)
		seedStringEdited = re.sub("leafNum", "n", seedStringEdited)
		seedStringEdited = re.sub("t\*", "e*", seedStringEdited)

	
	if stdString != []:
		## this would allow Houdini to dynamically determine the percentDeviation
		# stdStringEdited = re.sub("percentDeviation", "c", stdString)

		## this is just being rigidly honest to the L-Py code
		stdStringEdited = re.sub("percentDeviation", str(metas["percentDeviation"]), stdString)
		stdStringEdited = re.sub("mean", meanString, stdStringEdited)


	polyString = ""

	if gauss != None:
		 #group 2 is in case there's math after the function, like gauss(mean,std,seed) / 2.0
		polyString = "(gauss(" + meanString + "," + stdStringEdited + "," + seedStringEdited + ")" + gauss.group(3) + ")"
	elif uniform != None:
		polyString = "uniform(" + meanString + "," + stdStringEdited + "," + seedStringEdited + ")"
	elif poly != None:
		polyString = "poly(" + meanString + "," + stdStringEdited + "," + seedStringEdited + ")"
	elif random != None:
		polyString = "(rand(" + seedStringEdited + ")" + random.group(1) + ")"
	else:
		polyString = "(" + returnString + ")"


	return polyString


def getFunctions(lpyFile, metas):

	funcList = []
	line = ""
	endFuncs = None

	while endFuncs == None:
		defMatch = re.match("def (.+?)\((.+?)\):", line)
		if defMatch != None:
			funcName = defMatch.group(1)
			#funcArgs = re.split(",",defMatch.group(2))

			loop = True
			seedString = []
			meanString = []
			stdString = []
			returnString = []

			while loop == True:
				funcLine = lpyFile.next()
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

			funcMath = polynomialString(returnString, meanString, stdString, seedString, metas)

			funcList.append((funcName,funcMath))

		line = lpyFile.next()
		endFuncs = re.search("(.*)#CIS_BEGIN_RULES(.*)",line)

	return funcList


def getRules(lpyFile):

	line = lpyFile.next()

	while re.search("(.*)production(.*)",line) == None:
		line = lpyFile.next()
	line = lpyFile.next()

	ruleText = ""
	while re.search("(.*)endlsystem(.*)",line) == None:
		ruleText = ruleText + line
		line = lpyFile.next()

	rules = re.split("([A-Z]\(t\):)|(if.*t.*:)",ruleText)
	rules = filter(None,rules)

	houdiniRule = ""
	houdiniRules = []
	for i in range(len(rules)):
		name = re.search("[A-Z]\(t\):",rules[i])
		if name != None:
			houdiniRule = re.sub("t", "e", name.group(0)) # houdini uses 'e' instead of 't' to determine progress.
			nextName = None
			secondConditional = False
			while nextName == None:
				useif = re.search("if t(.*):",rules[i])
				if useif != None:
					if secondConditional == False:
						houdiniRule = houdiniRule + "t" + useif.group(1) + " = "
						secondConditional = True
					else:
						houdiniRules.append(houdiniRule)
						houdiniRule = re.sub("t", "e", name.group(0)) + "t" + useif.group(1) + " = "
				produce = re.search("produce(.*)",rules[i])
				if produce != None:
					houdiniRule = houdiniRule + produce.group(1) + "\n"
				i = i+1
				if i < len(rules):
					nextName = re.search("[A-Z]\(t\):",rules[i])
				else:
					nextName = "exit"



			houdiniRules.append(houdiniRule)

	return houdiniRules


def funcReplace(line, functionList):

	for item in functionList:
	    if item[0] in line:
	        line = line.replace(item[0],item[1])
	return line

def houdiniFuncReplace(funcname,funcArgs):
    global seedoff, seedincr

    args = funcArgs
    repl = ""

    try:
        myseedvar = seedvar
        if funcname == 'gauss':
            mean, std = args[0:2]
            if len(args) > 2:
                myseedvar = args[2]

            offset = "(" + mean + "-" + str(0.5*ngauss) + ")"
            # the variance of a 0..1 uniform distribution is 1/12.
            # The variance of the sum of ngauss of those is ngauss/12, or std dev = sqrt(ngauss/12).
            # Scale to suit.
            
            scale = "((" + std + ")*" + str(math.sqrt(ngauss/12.)) + ")"
            terms = []
            for i in range(ngauss):
                terms.append( "rand(%s+%d)" % (myseedvar, seedoff) )
                seedoff += seedincr
            randcenter = "(" + "+".join(terms) + "-2)/2"
            repl = "%s+%s*(%s)" % (mean,scale, randcenter) 

        elif funcname == 'uniform':
            vmax = float(args[0])
            vmin = 0
            if len(args)>1:
                vmin = float(args[1])
            if len(args)>2:
                myseedvar = args[2]
                offset = 0.5*(vmax+vmin)
                scale = 0.5*(vmax-vmin)
                repl = "%g+%g*rand(%s+%d)" % (offset,scale,myseedvar,seedoff)
                seedoff += seedincr

        elif funcname == 'poly4':
            #a, b, c, d = map(float, args[0:3])
            a = args[0]
            b = args[1]
            c = args[2]
            d = args[3]
            myseedvar = args[4]
            repl = "(" + a + "+" + b + "*" + myseedvar + "+" + c + "*" + myseedvar + "*" + myseedvar + "+" + d + "*" + myseedvar + "*" + myseedvar + "*" + myseedvar + ")"

        else:
        	repl = funcname + "("
        	for arg in funcArgs:
        		repl = repl + arg
        	repl = repl + ")"

        return repl

    except ValueError, e:
        raw = "%s(%s)" % (funcname, "".join(pieces[1:]))
        print >>sys.stderr, "Trouble parsing: ", raw
        print >>sys.stderr, pieces
        print >>sys.stderr, e
        return raw # unchanged, and inedible


def houdiniReplace(string, funcName):
    funcArgs = []

    index = 0
    storedChars = ""

    while index < len(string):

        if string[index] == "(":
            newfuncName = storedChars
            houdiniVals = houdiniReplace(string[index+1:],newfuncName)
            index = houdiniVals[0] + index + 1
            storedChars = houdiniVals[1]
        elif string[index] == ")":
            funcArgs.append(storedChars)
            return (index + 1, houdiniFuncReplace(funcName,funcArgs))
        elif string[index] == ",":
            funcArgs.append(storedChars)
            storedChars = ""
            index = index + 1
        else:
            storedChars = storedChars + string[index]
            index = index + 1

    print "hey it's me, your storedChars are " + storedChars
    return (index, storedChars)


with open(infname) as f:
    with open(outfname, 'w') as outf:
		metas = getMetas(f)
		print "exited metaBuilder"
		functionList = getFunctions(f, metas)
		print "exited functionBuilder"
		ruleList = getRules(f)
		print "exited rulesBuilder"

		print functionList
		for rule in ruleList:
			# continue with Stuart's code across the rules lines
	  		nrule = ""
	   		if rule[:1] == '#':
				nrule = rule
			else:
				rule = funcReplace(rule, functionList)
				print "rule replacing pseudos with functions "
				print rule
				print ""
				nrule = houdiniReplace(rule,"")[1] #myfuncs.sub( subfunc, rule )
				print "functions expanded for houdini "
				print nrule
				print ""
			print >>outf, nrule,

