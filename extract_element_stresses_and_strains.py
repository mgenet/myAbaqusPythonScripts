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

data_file = open(odb_basename + '.element_stresses_and_strains.dat', 'w')
data_file.write('# t E S\n')

for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        t = step.totalTime + frame.frameValue
        #print t
        data_file.write(str(t))

        if ('LE' in frame.fieldOutputs.keys()):
            field = frame.fieldOutputs['LE']
        else:
            field = frame.fieldOutputs['E']
        E = field.getSubset(region=element).values[gauss_number].data
        #print E
        nb_vec = len(E)
        if (nb_vec == 3): nb_dim = 2
        if (nb_vec == 6): nb_dim = 3
        for k in range(nb_dim        ): data_file.write(' ' + str(E[k]))
        for k in range(nb_dim, nb_vec): data_file.write(' ' + str(E[k]/2))

        field = frame.fieldOutputs['S']
        S = field.getSubset(region=element).values[gauss_number].data
        #print S
        for Sij in S: data_file.write(' ' + str(Sij))

        data_file.write('\n')

data_file.close()

odb.close()
