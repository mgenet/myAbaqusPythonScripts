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

node_numbers = [1694,681,2310,649]

pos = [numpy.array(instance.nodes[node_number].coordinates) for node_number in node_numbers]

disp_ED = [numpy.array(odb.steps["Step-1"].frames[-1].fieldOutputs['U'].getSubset(region=instance.nodes[node_number]).values[0].data) for node_number in node_numbers]
disp_ES = [numpy.array(odb.steps["Step-2"].frames[-1].fieldOutputs['U'].getSubset(region=instance.nodes[node_number]).values[0].data) for node_number in node_numbers]

#print pos
#print disp_ED
#print disp_ES

x1 = pos[1] - pos[0]
x1 = x1[0:2]
x1 /= numpy.linalg.norm(x1)

y1 = numpy.array([-x1[1], x1[0]])

z1 = pos[1]+disp_ED[1] - pos[0]-disp_ED[0]
z1 = z1[0:2]
z1 /= numpy.linalg.norm(z1)

theta1 = math.atan2(numpy.dot(z1, y1), numpy.dot(z1, x1)) * 180/math.pi

x1 = pos[3] - pos[2]
x1 = x1[0:2]
x1 /= numpy.linalg.norm(x1)

y1 = numpy.array([-x1[1], x1[0]])

z1 = pos[3]+disp_ED[3] - pos[2]-disp_ED[2]
z1 = z1[0:2]
z1 /= numpy.linalg.norm(z1)

theta2 = math.atan2(numpy.dot(z1, y1), numpy.dot(z1, x1)) * 180/math.pi

theta_ED = (theta1 + theta2)/2

x1 = pos[1] - pos[0]
x1 = x1[0:2]
x1 /= numpy.linalg.norm(x1)

y1 = numpy.array([-x1[1], x1[0]])

z1 = pos[1]+disp_ES[1] - pos[0]-disp_ES[0]
z1 = z1[0:2]
z1 /= numpy.linalg.norm(z1)

theta1 = math.atan2(numpy.dot(z1, y1), numpy.dot(z1, x1)) * 180/math.pi

x1 = pos[3] - pos[2]
x1 = x1[0:2]
x1 /= numpy.linalg.norm(x1)

y1 = numpy.array([-x1[1], x1[0]])

z1 = pos[3]+disp_ES[3] - pos[2]-disp_ES[2]
z1 = z1[0:2]
z1 /= numpy.linalg.norm(z1)

theta2 = math.atan2(numpy.dot(z1, y1), numpy.dot(z1, x1)) * 180/math.pi

theta_ES = (theta1 + theta2)/2

theta_ED_ES = theta_ES - theta_ED

print theta_ED
print theta_ES
print theta_ED_ES

odb.close()

### ----------------------------------------------------- ### OUTPUT ###

#open(odb_basename+'.opening_angle.dat', 'w').write(str(theta))
