#! /usr/bin/env python

import os
import sys
import re
import math
##import pyparsing as pp  # pyparsing.py package included in this directory, or 'pip install pyparsing'

# Read rules,
#   replace gauss(mean,std) with sum-of-uniform with unique t+N seed,
#   replace uniform(max[,min]) with scaled uniform with unique t+N seed

# Also accepts meta-directives:
# @seed  <seedvariable>
# and probably others

seedvar = "t"

outfname = None
polyfname = None

if len(sys.argv) <= 1:
    print >>sys.stderr, "Usage: %s [-o outfile.txt] [-p polynomialfile.txt]   infile.txt" % sys.argv[0]
    print >>sys.stderr, "Without -o, writes to infile_houdini.txt."
    print >>sys.stderr, "Without -p, reads polynomials from M_polynomials.txt"
    sys.exit(1)

ii = 1
while len(sys.argv) > ii and sys.argv[ii][0] == '-':
    arg = sys.argv[ii]; ii += 1
    if arg == '-o':
	outfname = sys.argv[ii]; ii += 1
    elif arg == '-p':
	polyfname = sys.argv[ii]; ii += 1

infname = sys.argv[ii]

if outfname is None:
    outfname = os.path.splitext(infname)[0] + "_houdini.txt"
if polyfname is None:
    polyfname = "M_polynomials.txt" # "/sd0/plantsinsilico/plant/rules/M_polynomials.txt"


print >>sys.stderr, "Processing %s into %s using %s" % (infname, outfname, polyfname)

class Replacer:

    items = ['pet.1Angle','pet.2Angle','mid-ifAngle','Left_angle','Right_angle','Middle_angle','internode','pet.1','pet.2','lat1L','lat1W','lat2L','lat2W','midL','midW','branchAngle','branchNodes','branchStart','branchEnd','numPods','numPodsAmbient']

    def __init__(self, polyfname, myfuncs, subfunc):

	# just scan the polynomial file once
	self.funcList = []
	with open(polyfname, 'r') as funcFile:
	    for funcline in funcFile:
		if funcline[:1] != '#':
		    str = funcline.split()[3]
		    while 1:
			newstr = myfuncs.sub( subfunc, str )
			if newstr == str:
			    break
			str = newstr
		    # Hack allowing { ... } to be in arguments to a gauss() etc call - special case for gauss(poly(...))
		    newstr = newstr.replace('{','(').replace('}',')')
		    self.funcList.append( newstr )

    def funcReplace(self, line):

	for i,item in enumerate(self.items):
	    if item in line:
		line = line.replace(item,self.funcList[i])
	return line

# Just scan for the things we know about.


myfuncs = re.compile( r'(gauss|uniform|poly)\(([^()]+)*\)' )

ngauss = 4

seedoff = 100
seedincr = 100

def subfunc(ma):
    # Accepts a match to a 'myfuncs' regex,
    # returns corresponding string
    global seedoff, seedincr

    pieces = ma.groups()
    funcname = pieces[0]
    args = pieces[1].split(',')

    try:
	myseedvar = seedvar
	if funcname == 'gauss':
	    mean, std = args[0:2]
	    if len(args) > 2:
		myseedvar = args[2]

	    offset = "(" + mean + "-" + str(0.5*ngauss) + ")"
	    # the variance of a 0..1 uniform distribution is 1/12.
	    # The variance of the sum of ngauss of those is ngauss/12, or std dev = sqrt(ngauss/12).
	    # Scale to suit.
	    
	    scale = "((" + std + ")*" + str(math.sqrt(ngauss/12.)) + ")"
	    terms = []
	    for i in range(ngauss):
		terms.append( "rand(%s+%d)" % (myseedvar, seedoff) )
		seedoff += seedincr
	    randcenter = "(" + "+".join(terms) + "-2)/2"
	    repl = "%s+%s*(%s)" % (mean,scale, randcenter) 

	elif funcname == 'uniform':
	    vmax = float(args[0])
	    vmin = 0
	    if len(args)>1:
		vmin = float(args[1])
	    if len(args)>2:
		myseedvar = args[2]
	    offset = 0.5*(vmax+vmin)
	    scale = 0.5*(vmax-vmin)
	    repl = "%g+%g*rand(%s+%d)" % (offset,scale,myseedvar,seedoff)
	    seedoff += seedincr

	elif funcname == 'poly':
	    #a, b, c, d = map(float, args[0:3])
	    a = args[0]
	    b = args[1]
	    c = args[2]
	    d = args[3]
	    myseedvar = args[4]
	    repl = "{" + a + "+" + b + "*" + myseedvar + "+" + c + "*" + myseedvar + "*" + myseedvar + "+" + d + "*" + myseedvar + "*" + myseedvar + "*" + myseedvar + "}"

	return repl

    except ValueError, e:
	raw = "%s(%s)" % (funcname, "".join(pieces[1:]))
	print >>sys.stderr, "Trouble parsing: ", raw
	print >>sys.stderr, pieces
	print >>sys.stderr, e
	return raw # unchanged, and inedible
	

replacer = Replacer( polyfname, myfuncs, subfunc )

with open(infname) as f:
    with open(outfname, 'w') as outf:
	for line in f.readlines():
	    nline = ""
	    if line[:1] == '#':
		nline = line
	    else:
		nline = replacer.funcReplace(line)
	        #nline = myfuncs.sub( subfunc, line )
	    print >>outf, nline,
