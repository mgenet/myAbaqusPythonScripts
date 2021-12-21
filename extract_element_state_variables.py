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

if (len(sys.argv) > 2):
    elem_number = int(sys.argv[2])
else:
    elem_number = 0

if (len(sys.argv) > 3):
    gauss_number = int(sys.argv[3])
else:
    gauss_number = 0

### ------------------------------------------------- ### EXTRACTION ###

odb           = odbAccess.openOdb(path=odb_basename + '.odb')
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]
element       = instance.elements[elem_number]

data_file = open(odb_basename + '.element_state_variables.dat', 'w')
data_file.write('# t sdvs\n')

for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        t = step.totalTime + frame.frameValue
        #print t
        data_file.write(str(t))

        nb_sdv = sum(['SDV' in field_name for field_name in frame.fieldOutputs.keys()])
        #print "nb_sdv = " + str(nb_sdv)
        for i in range(1,nb_sdv+1):
            field = frame.fieldOutputs['SDV'+str(i)]
            SDV = field.getSubset(region=element).values[0].data
            #print SDV
            data_file.write(' ' + str(SDV))

        data_file.write('\n')

data_file.close()

odb.close()
