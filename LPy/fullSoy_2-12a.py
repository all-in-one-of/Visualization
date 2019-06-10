### BASIC SOYPLANT LSYSTEM DEFINITION IN L-PY

###########################
## Python Functions here ##
###########################

import random

totalPlants = 500
percentDeviation = 0.1
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

def defaultStd(mean):
	return mean * percentDeviation

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

def pet1Angle(t):
	#approx 40
	random.seed(t*totalPlants+plantId)
	mean = poly4(72.6898,-9.47077,0.604073,-0.014325,t)
 	std = defaultStd(mean)
	return random.gauss(mean,std)

def pet1Len(t):
	#approx 100
	random.seed(t*totalPlants+plantId)
	mean = poly4(18.9256,71.5597,-7.65314,0.203292,t)
	std = defaultStd(mean)
	return random.gauss(mean,std)

def rightAngle(t):
	#approx 100
	random.seed(t*totalPlants+plantId)
	return random.random()*78.506 + 56.933

def pet2Angle(t,leafNum):
	#approx 175
	random.seed(t*totalPlants*3+plantId*3+leafNum)
	mean = 175
	std = defaultStd(mean)
	return random.gauss(mean,std)

def pet2Len(t,leafNum):
	#approx 34
	random.seed(t*totalPlants*3+plantId*3+leafNum)
	mean = poly4(1.85862,10.5498,-1.05534,0.0328947,t)
	std = defaultStd(mean)
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

def leafScale(t,leafNum):
	#approx 80
	random.seed(t*totalPlants+plantId)
	if leafNum == 1: # lat1L and lat1W
		meanL = poly4(11.5486,20.4316,-1.3487,0.0108518,t)
		stdL = defaultStd(meanL)
		meanW = poly4(3.66584,17.0814,-1.52372,0.0304085,t)
		stdW = defaultStd(meanW)
		length = random.gauss(meanL,stdL)
		width = random.gauss(meanW,stdW)
		return length
	elif leafNum == 2: # midL and midW
		meanL = poly4(48.3914,11.1378,-0.445903,-0.0149725,t)
		stdL = defaultStd(meanL)
		meanW = poly4(33.5568,5.39565,-0.252362,-0.0120859,t)
		stdW = defaultStd(meanW)
		length = random.gauss(meanL,stdL)
		width = random.gauss(meanW,stdW)
		return length
	else: #leafNum == 3 # lat2L and lat2W
		meanL = poly4(13.4182,21.072,-1.59109,0.0223835,t)
		stdL = defaultStd(meanL)
		meanW = poly4(8.72296,13.4351,-1.01909,0.0122768,t)
		stdW = defaultStd(meanW)
		length = random.gauss(meanL,stdL)
		width = random.gauss(meanW,stdW)
		return length

def cotyLen(t):
	#not in data
	return 25

##########################
## Begin LSystem syntax ##
##########################

Axiom:  SetWidth(rad(1)) B(1)

derivation length: 16

production:

B(t):
	produce \(90)F(half(t),rad(t))\(90)F(half(t),rad(t)) [+(pet1Angle(t)) F(cotyLen(t)) T(t) ;;;@O(5)] [-(pet1Angle(t)) F(cotyLen(t)) T(t) ;;;@O(5)] A(t+1) 

A(t):
	if t<=2:
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [+(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leafScale(t,2))] [-(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leafScale(t,2))] A(t+1)

	else:
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t,1)) F(pet2Len(t,1)) T(t) +(180-midifAngle(t)) \(90);~l(leafScale(t,1))]  [!^(leftAngle(t))-(180-pet2Angle(t,2)) F(pet2Len(t,2)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t,2))]  [!&(middleAngle(t))-(180-pet2Angle(t,3)) F(pet2Len(t,3)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t,3))]]   [-(branchAngle(t)) \(90)Z(t)]    [-(15)&(45) F(10) T(t) ;;;@O(3)]  A(t+1)


Z(t):
	if t<=6:  # highest number internode to grow a branch from
		produce V(1)
		
V(t):
  if t<=4:  # number of generations to grow branches for
  		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t,1)) F(pet2Len(t,1)) T(t) +(180-midifAngle(t)) \(90);~l(leafScale(t,1))]  [!^(leftAngle(t))-(180-pet2Angle(t,2)) F(pet2Len(t,2)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t,2))]  [!&(middleAngle(t))-(180-pet2Angle(t,3)) F(pet2Len(t,3)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t,3))]]   [-(15)&(45) F(10) T(t) ;;;@O(3)]  V(t+1)

T(t):  # create a tapered tip
	produce F(4,0)

endlsystem

