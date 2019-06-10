### BASIC SOYPLANT LSYSTEM DEFINITION IN L-PY

###########################
## Python Functions here ##
###########################

# Variable 't' indicates time

def getCarbon(t):
	return 1

# get cross-sectional radius
def rad(t):
	#return 4.0/(t/10+1)
	return 5

# get internode length
def ilen(t):
	return 25

# get half the internode length
def half(t):
	return ilen(t)/2.0

def pet1Angle(t):
	return 40

def pet1Len(t):
	return 100

def rightAngle(t):
	return 100

def pet2Angle(t):
	return 175

def pet2Len(t):
	return 34

def midifAngle(t):
	return 180

def leftAngle(t):
	return 100

def middleAngle(t):
	return 10

def branchAngle(t):
	return 49

def leafScale(t):
	return 50

def cotyLen(t):
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
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [+(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leafScale(t))] [-(pet1Angle(t)) F(cotyLen(t)) T(t) \(90);~l(leafScale(t))] A(t+1)

	else:
		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t)) F(pet2Len(t)) T(t) +(180-midifAngle(t)) \(90);~l(leafScale(t))]  [!^(leftAngle(t))-(180-pet2Angle(t)) F(pet2Len(t)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t))]  [!&(middleAngle(t))-(180-pet2Angle(t)) F(pet2Len(t)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t))]]   [-(branchAngle(t)) \(90)Z(t)]    [-(15)&(45) F(10) T(t) ;;;@O(3)]  A(t+1)


Z(t):
	if t<=6:  # highest number internode to grow a branch from
		produce V(1)
		
V(t):
  if t<=4:  # number of generations to grow branches for
  		produce \(90) F(half(t),rad(t)) \(90) F(half(t),rad(t)) [-(pet1Angle(t)) ! F(pet1Len(t)) [!&(rightAngle(t))+(180-pet2Angle(t)) F(pet2Len(t)) T(t) +(180-midifAngle(t)) \(90);~l(leafScale(t))]  [!^(leftAngle(t))-(180-pet2Angle(t)) F(pet2Len(t)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t))]  [!&(middleAngle(t))-(180-pet2Angle(t)) F(pet2Len(t)) T(t) -(180-midifAngle(t)) \(90);~l(leafScale(t))]]   [-(15)&(45) F(10) T(t) ;;;@O(3)]  V(t+1)

T(t):  # create a tapered tip
	produce F(4,0)

endlsystem

