import math

myString = "gauss(poly(1.85862,10.5498,-1.05534,0.0328947,e),poly(1.85862,10.5498,-1.05534,0.0328947,e)*c,e*500*3+b*3+n)"

seedvar = "t"
ngauss = 4
seedoff = 100
seedincr = 100

def houdiniFuncReplace(funcname,funcArgs):
    global seedoff, seedincr

    args = funcArgs
    repl = ""

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
            repl = "(" + a + "+" + b + "*" + myseedvar + "+" + c + "*" + myseedvar + "*" + myseedvar + "+" + d + "*" + myseedvar + "*" + myseedvar + "*" + myseedvar + ")"

        return repl

    except ValueError, e:
        raw = "%s(%s)" % (funcname, "".join(pieces[1:]))
        print >>sys.stderr, "Trouble parsing: ", raw
        print >>sys.stderr, pieces
        print >>sys.stderr, e
        return raw # unchanged, and inedible

def houdiniReplace(string, funcName, depth):
    funcArgs = []

    index = 0
    storedChars = ""

    while index < len(string):

        if string[index] == "(":
            newfuncName = storedChars
            houdiniVals = houdiniReplace(string[index+1:],newfuncName, depth +1)
            index = houdiniVals[0] + index + 1
            storedChars = houdiniVals[1]
        elif string[index] == ")":
            funcArgs.append(storedChars)
            return (index + 1, houdiniFuncReplace(funcName,funcArgs))
        elif string[index] == ",":
            funcArgs.append(storedChars)
            storedChars = ""
            index = index + 1
        else:
            storedChars = storedChars + string[index]
            index = index + 1

    return (index, storedChars)


print houdiniReplace(myString,"",0)[1]













