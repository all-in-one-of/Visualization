def alpha(x):
  return 30  # try other decreasing functions ex: 30-10*x 

def long(x):  
  return 1   # try other decreasing functions ex: 50/(x*x) ; 2-x/6+1 


Axiom: A(1)

production:

derivation length: 6

A(n) :
  produce F(long(n))[+(alpha(n))A(n+1)] [-(alpha(n))A(n+1)]F(0.2);(3)@O(0.2)

endlsystem