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

###                                                      ###############
### ---------------------------------------------------- ### imports ###
###                                                      ###############

import os
import sys
sys.path.append(os.getcwd())

import odbAccess

from CompMechTools.Cell.Utils import *

###                                               ######################
### --------------------------------------------- ### initialization ###
###                                               ######################

cell = create_cell(sys.argv[1])
if (len(sys.argv) > 3): cell.set_mesh_parameters_from_argv(sys.argv[3:])
cell.set_bounding_box()
cell.set_faces()

odb_basename = sys.argv[1]
odb_name     = odb_basename + '.odb'
odb          = odbAccess.openOdb(path=odb_name)

step   = odb.steps['Step-1']
frames = step.frames

root_assembly   = odb.rootAssembly
instance        = root_assembly.instances['PART-1-1']

loading_direction = int(sys.argv[2])

if   (loading_direction == 0): border = instance.nodeSets['NODES_XMAX']
elif (loading_direction == 1): border = instance.nodeSets['NODES_YMAX']
elif (loading_direction == 2): border = instance.nodeSets['NODES_ZMAX']

###                                                       ##############
### ----------------------------------------------------- ### script ###
###                                                       ##############

strength = 0.

for frame in frames:
    t = frame.frameValue
    #print t

    field = frame.fieldOutputs['RF']
    F = 0.
    for value in field.getSubset(region=border).values:
        F += value.data[loading_direction]
    sig = F / cell.S[loading_direction]
    #print sig

    strength = max(strength, sig)

odb.close()

savefile = open(cell.get_name() + '_strength.dat', 'w')
savefile.write(str(strength))
savefile.close()
