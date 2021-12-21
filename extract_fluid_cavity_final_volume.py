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

### ---------------------------------------------------------------- ###

import sys

import odbAccess

### ---------------------------------------------------------------- ###

odb_basename = sys.argv[1]

if (len(sys.argv) > 2):
    num_history_region = int(sys.argv[2])
else:
    num_history_region = 0

### ---------------------------------------------------------------- ###

odb = odbAccess.openOdb(path=odb_basename+'.odb')
step = odb.steps[odb.steps.keys()[-1]]
volume = step.historyRegions[step.historyRegions.keys()[num_history_region]].historyOutputs['CVOL'].data[-1][1]

open(odb_basename + '.fluid_cavity_final_volume.dat', 'w').write(str(volume))
