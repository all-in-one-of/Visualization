import random as rd
 
stagelength = 2     # number of step between two verticille production
nbcycle = 20         # total number of verticille branches wanted 
minbranches = 4     # minimum number of branches when producing verticille
maxbranches = 8     # minimum number of branches when producing verticille
leafduration = 10   # life time of a leaf
leafmaturation = 3  # age at which a leaf is considered as old
branchfall = 14
angdev = 20         # authorized variation of angles to introduce some random
leafel = 50         # angle of leaf inclination from horizontal direction
radinc = 0.005      # increment of radius through time
 
def maxleafsize(s,maxs):      # maximum size of a leaf 
  return (s*0.5/float(maxs))+0.5
 
def leafsize(maxsize, t):     # size of a leaf according to its age
  if t < leafmaturation:
    return maxsize * ((t*0.5/float(leafmaturation))+0.5)
  else:
      return maxsize
 
def branch_angle(nc):         # branching angle according to position on trunk
    return 70+ 20*((nbcycle-nc)/float(nbcycle))
 
def branch_bending(time):     # branch bending as a function of time
    return time*1.7
 
module A # represent trunk apical meristem
module B # represent apical meristem of lateral branches
module L # whorl of leaf
module I # Internode
 
Axiom: SetWidth(0.1)I(0.5,0.1)A(-stagelength+1)
 
derivation length: nbcycle*stagelength -1
production:

A(t) :
  nproduce I(0.5,0.1)/(90)L(maxleafsize(t%stagelength,stagelength)*1.5,0) # produce a metamer
  if (t % stagelength) == 0:
      cyclenb = t // stagelength
      # produce a verticille of branches.
      nbaxe = rd.randint(minbranches,maxbranches)
      for i in xrange(nbaxe):
        nproduce [/(360*i/nbaxe)&(branch_angle(cyclenb))C(max(14-t, 0))B(0)]
  produce A(t+1)
  # produce apex with older age.
 
B(t) :          # growth of young metamer is faster than for old
  if t < 5:
    produce I(1,0.1)K(0)B(t+1)
  else :
    produce I(1*(1-(2*t/100)),0.1)
 
C(t):          # after some time the branch dies
  if t < branchfall :
    produce C(t+1)
  else :
    produce %
 
K(t) :
  # ages the branches leaves. If too old, removes
  if t <= leafduration :
    produce K(t+1)
  else:
    produce
 
L(maxsize,t) :
  # ages the trunk leaves. If too old, removes
  if t <= leafduration :
    produce L(maxsize,t+1)
  else:
    produce *  
 
I(s,r)--> I(s,r+radinc)
 
homomorphism:

I(l,r) --> SetWidth(r)F(l, r-radinc)
C(t) --> &(branch_bending(t))
L(maxsize,t) --> [&(120);(2)~l(leafsize(maxsize,t))][^(120);(2)~l(leafsize(maxsize,t))]
 
K(t) --> [+(rd.uniform(90-angdev, 90+angdev))&(rd.uniform(leafel-angdev, leafel+angdev));(2)~l(leafsize(1,t))][-(rd.uniform(90-angdev, 90+angdev))&(rd.uniform(leafel-angdev, leafel+angdev));(2)~l(leafsize(1,t))]
 
endlsystem