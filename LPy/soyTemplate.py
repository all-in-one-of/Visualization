# pure python here

module A  # new nodes
module B  # starting premise

Axiom: FF[+HJ][-HJ]A

derivation length: 12

production:

A(t):
	if t <= 2:
		produce "!FF[+TTHTK][-TTHTK]A
	elif t > 2 && t%2:
		produce "!FF[+TQ]A
	else:
		produce "!FF[-TQ]A

Q(t):
	nproduce Q=FTT[HTK][&&HTK][^^HTK]




endlsystem