import random as random


def rand(input):
	random.seed(input)
	return random.random()

e = 18
c = 0
b = 1
random.seed(e*500+b+100)
q = random.random()
random.seed(e*500+b+200)
r = random.random()
random.seed(e*500+b+300)
s = random.random()
random.seed(e*500+b+400)
t = random.random()
#f = (74.3715+-11.2832*e+0.933566*e*e+-0.0293258*e*e*e-2.0)+((74.3715+-11.2832*e+0.933566*e*e+-0.0293258*e*e*e*c)/0.57735026919)*(q+r+s+t)
#f = (74.3715+-11.2832*e+0.933566*e*e+-0.0293258*e*e*e*c)
#f = 18.9256 + 71.5597*e +-7.65314*e*e + 0.203292*e*e*e
f = 18.9256+71.5597*e+-7.65314*e*e+0.203292*e*e*e+((18.9256+71.5597*e+-7.65314*e*e+0.203292*e*e*e*c)*0.57735026919)*((rand(e*500+b+100)+rand(e*500+b+200)+rand(e*500+b+300)+rand(e*500+b+400)-2)/2)
#f = 18.9256+71.5597*e+-7.65314*e*e+0.203292*e*e*e
print f

