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
