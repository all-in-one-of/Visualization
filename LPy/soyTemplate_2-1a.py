### BASIC SOYPLANT LSYSTEM DEFINITION IN L-PY

###########################
## Python Functions here ##
###########################

# Variable 't' indicates time

def getCarbon(t):
	return 1

# get internode length
def ilen(t):
	return 1

# get half the internode length
def half(t):
	return ilen(t)/2.0


##########################
## Begin LSystem syntax ##
##########################

Axiom: A(1)

derivation length: 12

production:

A(t):
	produce F(ilen(t))F(ilen(t))[+F(half(t))@O(0.2)][-F(half(t))@O(0.2)]B(t+1)

B(t):
	if t<=2:
		produce FB
	else:
		produce FFFB


endlsystem

# Houdini basic soyplant rules
# B = FF[+HJ][-HJ]A
# A:t<=2 = "!FF[+TTH//TK][-TTH\\TK]A
# A:(t>2)&(t%2) = "!FF[+TQ]A
# A:(t>2)&((t%2)+1) = "!FF[-TQ]A
# Q=FTT//[--HTK][++HTK][HTK]
# R=FTT\\[--HTK][++HTK][HTK]