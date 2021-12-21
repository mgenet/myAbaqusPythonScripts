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

import odbAccess

### ----------------------------------------------------- ### INPUTS ###

odb_basename = sys.argv[1]
odb = odbAccess.openOdb(path=odb_basename + '.odb')

if (len(sys.argv) > 2):
    step_name = sys.argv[2]
else:
    step_name = odb.steps.keys()[-1]

if (len(sys.argv) > 3):
    num_frame = int(sys.argv[3])
else:
    num_frame = -1

### ------------------------------------------------- ### EXTRACTION ###

coords = [value.data for value in odb.steps[step_name].frames[num_frame].fieldOutputs["COORD"].values]

### ----------------------------------------------------- ### OUTPUT ###

open(odb_basename+'.'+os.path.basename(__file__)[8:-3]+'.dat','w').write("\n".join([", ".join([str(comp) for comp in coord]) for coord in coords]))
