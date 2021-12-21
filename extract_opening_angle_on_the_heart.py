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
import numpy

import odbAccess

### ----------------------------------------------------- ### INPUTS ###

odb_basename = sys.argv[1]

### ------------------------------------------------- ### EXTRACTION ###

odb           = odbAccess.openOdb(path=odb_basename + '.odb')
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]

pos = [odb.steps[odb.steps.keys()[-1]].frames[-1].fieldOutputs['COORD'].getSubset(region=instance.nodes[node_number]).values[0].data for node_number in [3349, 4015, 4045, 4099, 4369]]

#print "pos = " + str(pos)

v1i = pos[1]-pos[0]
v1o = pos[2]-pos[0]
v2i = pos[3]-pos[0]
v2o = pos[4]-pos[0]

v1i /= numpy.linalg.norm(v1i)
v1o /= numpy.linalg.norm(v1o)
v2i /= numpy.linalg.norm(v2i)
v2o /= numpy.linalg.norm(v2o)

#print "v1i = " + str(v1i)
#print "v1o = " + str(v1o)
#print "v2i = " + str(v2i)
#print "v2o = " + str(v2o)

thetai = math.acos(numpy.dot(v1i, v2i)) * 180/math.pi
thetao = math.acos(numpy.dot(v1o, v2o)) * 180/math.pi

print "thetai = " + str(thetai)
print "thetao = " + str(thetao)

theta = (thetai + thetao) / 2

print "theta = " + str(theta)

odb.close()

### ----------------------------------------------------- ### OUTPUT ###

#open(odb_basename+'.opening_angle.dat', 'w').write(str(theta))
