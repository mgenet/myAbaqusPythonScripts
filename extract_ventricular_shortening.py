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

basal_nodes = instance.nodeSets['N-BASEDG'].nodes
basal_height = numpy.mean([node.coordinates[2] for node in basal_nodes])

#print "basal_height = " + str(basal_height)

apical_nodes_numbers = [1694,681,2310,649]
apical_nodes = [instance.nodes[node_number] for node_number in apical_nodes_numbers]
apical_height = numpy.mean([node.coordinates[2] for node in apical_nodes])

#print "apical_height = " + str(apical_height)

length = basal_height - apical_height

#print "length = " + str(length)

disp_ED = numpy.mean([odb.steps["Step-1"].frames[-1].fieldOutputs['U'].getSubset(region=node).values[0].data[2] for node in apical_nodes])
disp_ES = numpy.mean([odb.steps["Step-2"].frames[-1].fieldOutputs['U'].getSubset(region=node).values[0].data[2] for node in apical_nodes])

#print "disp_ED = " + str(disp_ED)
#print "disp_ES = " + str(disp_ES)

stretch_ED = -100*disp_ED/length
stretch_ES = -100*disp_ES/length
stretch_ED_ES = stretch_ES-stretch_ED

print "stretch_ED = " + str(stretch_ED)
print "stretch_ES = " + str(stretch_ES)
print "stretch_ED_ES = " + str(stretch_ED_ES)

odb.close()

### ----------------------------------------------------- ### OUTPUT ###

#open(odb_basename+'.opening_angle.dat', 'w').write(str(theta))
