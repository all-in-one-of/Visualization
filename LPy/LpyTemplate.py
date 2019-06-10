# pure python code
def func():
   # python code
   nproduce lstring # it is possible to use the nproduce statement 
                    # in this part of the file
 
module A,B   # declaration of module name
 
Axiom: lstring # declaration of axiom
 
derivation length: int # default = 1
                       # number of derivation step to perform
production: # beginning of production rules
 
pattern :          # a production rule. Start with successor given as a pattern of module to replace
   python code     # rule core are pure python code with production statement
   produce lstring # production statement giving the new string pattern to produce
 
# simple rules can be expressed this way
pattern --> new_pattern
 
homomorphism: # beginning of homomorphism rules. 
              # They are called before plotting the string or 
              # application of rule with query modules (?[PHUR])
maximum depth: int # default = 1
                   # number of homomorphism recursive step to perform.
                   # should be defined only once
 
decomposition: # beginning of decomposition rules.
               # These rules are applied recursively after each production step
               # usefull to decompose a module into a structure
maximum depth: int # default = 1
                   # number of decomposition recursive step to perform.
                   # should be defined only once
 
group: int  # all following rules will be assign to this group
            # to activate a group of rule see command useGroup
            # by default group 0 is active
 
production: # again all types of rule can be defined
homomorphism:
decomposition:
 
endgroup # following rules will be assign to default 0 group
 
production: # again all types of rule can be defined
homomorphism:
decomposition:
 
endlsystem # end of rules definition
 
# pure python code is again possible