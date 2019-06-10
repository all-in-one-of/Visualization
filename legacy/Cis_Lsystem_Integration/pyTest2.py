import re

lpyFile = open("./fileText2.py", 'r')

def getRules(lpyFile):
	line = next(lpyFile)

	while re.search("(.*)production(.*)",line) == None:
		line = next(lpyFile)
	line = next(lpyFile)

	ruleText = ""
	while re.search("(.*)endlsystem(.*)",line) == None:
		ruleText = ruleText + line
		line = next(lpyFile)

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


rules = getRules(lpyFile)
for i,rule in enumerate(rules):
	print "rule " + str(i) + " is:"
	print rule
print "length of rules list is: " + str(len(rules))