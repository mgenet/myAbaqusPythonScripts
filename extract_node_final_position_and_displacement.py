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

import sys

import odbAccess

### ----------------------------------------------------- ### INPUTS ###

odb_basename = sys.argv[1]
node_number = int(sys.argv[2])

### ------------------------------------------------- ### EXTRACTION ###

odb = odbAccess.openOdb(path=odb_basename + '.odb')
root_assembly = odb.rootAssembly
instance = root_assembly.instances[root_assembly.instances.keys()[0]]
node = instance.nodes[node_number-1]
position = node.coordinates
step = odb.steps[odb.steps.keys()[0]]
frame = step.frames[-1]
field = frame.fieldOutputs['U']
displacement = field.getSubset(region=node).values[0].data

#print "position = ", position
#print "displacement = ", displacement

### ----------------------------------------------------- ### OUTPUT ###

open(odb_basename + '.node_final_position.dat', 'w').write(str(position[0]) + ' ' + str(position[1]))
open(odb_basename + '.node_final_displacement.dat', 'w').write(str(displacement[0]) + ' ' + str(displacement[1]))
