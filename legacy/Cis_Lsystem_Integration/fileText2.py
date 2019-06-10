
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
