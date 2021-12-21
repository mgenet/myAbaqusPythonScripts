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
pressures = [data[1] for key in odb.steps.keys() for data in odb.steps[key].historyRegions[odb.steps[key].historyRegions.keys()[num_history_region]].historyOutputs['PCAV'].data]

### ---------------------------------------------------------------- ###

open(odb_basename+'.fluid_cavity_pressures.dat', 'w').write(str(pressures))
