#### NOTES: ilen and half probably need to be addressed.



### BASIC SOYPLANT LSYSTEM DEFINITION IN L-PY

###########################
## Python Functions here ##
###########################

import random
from openalea.plantgl.all import *
from math import * 

#CIS Specifically searches for "percentDeviation" and "totalPlants" as metas
percentDeviation = 0.1

totalPlants = 500
plantId = 1

# Variable 't' indicates time

def getCarbon(t):
	return 1

# get cross-sectional radius
def rad(t):
	#return 4.0/(t/10+1)
	return 5

def poly4(A,B,C,D,t):
	return A + B*t + C*t*t + D*t*t*t

# get internode length
def ilen(t):
	#approx 25	
	random.seed(t*totalPlants+plantId)
	mean = poly4(16.1642,9.23233,-0.403514,-0.00551854,t)
	std = poly4(4.17566,1.50607,0.0150387,-0.00581527,t)
	return random.gauss(mean, std)

# get half the internode length
def half(t):
	return ilen(t)/2.0

#CIS_BEGIN_FUNCTIONS

def pet1Angle(t):
	#approx 40
	random.seed(t*totalPlants+plantId)
	mean = poly4(72.6898,-9.47077,0.604073,-0.014325,t)
 	std = mean * percentDeviation
	return random.gauss(mean,std)

def pet1Len(t):
	#approx 100
	random.seed(t*totalPlants+plantId)
	mean = poly4(18.9256,71.5597,-7.65314,0.203292,t)
	std = mean * percentDeviation
	return random.gauss(mean,std)

def rightAngle(t):
	#approx 100
	random.seed(t*totalPlants+plantId)
	return random.random()*78.506 + 56.933

def pet2Angle(t,leafNum):
	#approx 175
	random.seed(t*totalPlants*3+plantId*3+leafNum)
	mean = 175
	std = mean * percentDeviation
	return random.gauss(mean,std)

def pet2Len(t,leafNum):
	#approx 34
	random.seed(t*totalPlants*3+plantId*3+leafNum)
	mean = poly4(1.85862,10.5498,-1.05534,0.0328947,t)
	std = mean * percentDeviation
	return random.gauss(mean,std)

def midifAngle(t):
	#approx 180
	random.seed(t*totalPlants+plantId)
	return random.random()*50 + 149

def leftAngle(t):
	#approx 100
	random.seed(t*totalPlants+plantId)
	return random.random()*76.798 + 59.187

def middleAngle(t):
	#approx 10
	random.seed(t*totalPlants+plantId)
	return random.random()*29.606 + 1.126

def branchAngle(t):
	#approx 49
	random.seed(t*totalPlants+plantId)
	mean = 49
	std = mean * 0.1
	return random.gauss(mean,std)

def leaf1Length(t):
	#approx 80
	#lat1L
	random.seed(t*totalPlants+plantId)
	mean = poly4(11.5486,20.4316,-1.3487,0.0108518,t)
	std = mean * percentDeviation 
	return random.gauss(mean,std)

def leaf1Width(t):
	#approx 80
	#lat1W
	random.seed(t*totalPlants+plantId)
	mean = poly4(3.66584,17.0814,-1.52372,0.0304085,t)
	std = mean * percentDeviation
	return random.gauss(mean,std)

def leaf2Length(t):
	#approx 80
	#lat2L
	random.seed(t*totalPlants+plantId)
	mean = poly4(48.3914,11.1378,-0.445903,-0.0149725,t)
	std = mean * percentDeviation 
	return random.gauss(mean,std)

def leaf2Width(t):
	#approx 80
	#lat2W
	random.seed(t*totalPlants+plantId)
	mean = poly4(33.5568,5.39565,-0.252362,-0.0120859,t)
	std = mean * percentDeviation
	return random.gauss(mean,std)

def leaf3Length(t):
	#approx 80
	#lat3L
	random.seed(t*totalPlants+plantId)
	mean = poly4(13.4182,21.072,-1.59109,0.0223835,t)
	std = mean * percentDeviation 
	return random.gauss(mean,std)

def leaf3Width(t):
	#approx 80
	#lat3W
	random.seed(t*totalPlants+plantId)
	mean = poly4(8.72296,13.4351,-1.01909,0.0122768,t)
	std = mean * percentDeviation
	return random.gauss(mean,std)

def cotyLen(t):
	#not in data
	return 25

##########################
## Begin LSystem syntax ##
##########################

#CIS_BEGIN_RULES

Axiom:  SetWidth(rad(1)) B(1)

derivation length: 16

production:

B(t):
	produce \(90)F(half(t),rad(t))\(90)F(half(t),rad(t)) [+(pet1Angle(t)) F(cotyLen(t)) T(t) ;;;@O(5)] [-(pet1Angle(t)) F(cotyLen(t)) T(t) ;;;@O(5)] A(t+1) 

A(t):
	if t<=2:
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [+(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leaf2Length(t))] [-(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leaf2Length(t))] A(t+1)

	if t>2:
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t,1)) F(pet2Len(t,1)) T(t) +(180-midifAngle(t)) \(90);~l(leaf1Length(t))]  [!^(leftAngle(t))-(180-pet2Angle(t,2)) F(pet2Len(t,2)) T(t) -(180-midifAngle(t)) \(90);~l(leaf2Length(t))]  [!&(middleAngle(t))-(180-pet2Angle(t,3)) F(pet2Len(t,3)) T(t) -(180-midifAngle(t)) \(90);~l(leaf3Length(t))]]   [-(branchAngle(t)) \(90)Z(t)]    [-(15)&(45) F(10) T(t) ;;;@O(3)]  A(t+1)


Z(t):
	if t<=6:  # highest number internode to grow a branch from
		produce V(1)
		
V(t):
  if t<=4:  # number of generations to grow branches for
  		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t,1)) F(pet2Len(t,1)) T(t) +(180-midifAngle(t)) \(90);~l(leaf1Length(t))]  [!^(leftAngle(t))-(180-pet2Angle(t,2)) F(pet2Len(t,2)) T(t) -(180-midifAngle(t)) \(90);~l(leaf2Length(t))]  [!&(middleAngle(t))-(180-pet2Angle(t,3)) F(pet2Len(t,3)) T(t) -(180-midifAngle(t)) \(90);~l(leaf3Length(t))]]   [-(15)&(45) F(10) T(t) ;;;@O(3)]  V(t+1)

T(t):  # create a tapered tip
	produce F(4,0)

endlsystem


########################
##   INITIALISATION   ##
########################

#this should allow you to use "Sweep(nerve,section,length,dl,x,width)" or some other function to replace ~l()

__lpy_code_version__ = 1.1

def __initialiseContext__(context):
	import openalea.plantgl.all as pgl
	width = pgl.NurbsCurve2D(	
	    ctrlPointList = pgl.Point3Array([(0, 0.0368034, 1),(0.321038, 0.20082, 1),(0.674863, 0.127049, 1),(1, 0.00418017, 1)]) , 
	    )
	width.name = "width"
	panel_0 = ({'active': True, 'visible': True, 'name': 'Functions'},[('Function',width)])
	import openalea.plantgl.all as pgl
	nerve = pgl.NurbsCurve2D(	
	    ctrlPointList = pgl.Point3Array([(-0.5, 0, 1),(-0.223915, 0.114315, 1),(0.121756, 0.0370409, 1),(0.467244, -0.216243, 1)]) , 
	    )
	nerve.name = "nerve"
	section = pgl.NurbsCurve2D(	
	    ctrlPointList = pgl.Point3Array([(-0.5, 0, 1),(-0.195355, -0.24554, 1),(0.203326, -0.162142, 1),(0.5, 0, 1)]) , 
	    )
	section.name = "section"
	panel_1 = ({'active': True, 'visible': True, 'name': 'Curve2D'},[('Curve2D',nerve),('Curve2D',section)])
	parameterset = [panel_0,panel_1,]
	context["__functions__"] = [('width',width),]
	context["__curves__"] = [('nerve',nerve),('section',section),]
	context["__parameterset__"] = parameterset
	context["width"] = pgl.QuantisedFunction(width)
	context["nerve"] = nerve
	context["section"] = section
