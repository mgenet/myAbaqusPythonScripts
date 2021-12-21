#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2008-2015                               ###
###                                                                  ###
### Laboratoire de Mécanique et de Technologie (LMT), Cachan, France ###
### Lawrence Berkeley National Laboratory, California, USA           ###
### University of California at San Francisco, USA                   ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
###                                                                  ###
########################################################################

### ---------------------------------------------------- ### IMPORTS ###

import os
import sys
import math

import odbAccess

### ----------------------------------------------------- ### INPUTS ###

odb_basename = sys.argv[1]

### ------------------------------------------------- ### EXTRACTION ###

odb           = odbAccess.openOdb(path=odb_basename + '.odb')
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]
node          = instance.nodes[0]
disp          = odb.steps[odb.steps.keys()[-1]].frames[-1].fieldOutputs['U'].getSubset(region=node).values[0].data
odb.close()

theta = 2 * math.atan(disp[1]/(20.+disp[0])) * 180./math.pi
print "theta = " + str(theta)

### ----------------------------------------------------- ### OUTPUT ###

#open(odb_basename+'.opening_angle.dat', 'w').write(str(theta))
