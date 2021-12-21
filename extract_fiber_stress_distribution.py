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

### ------------------------------------------------- ### EXTRACTION ###

odb           = odbAccess.openOdb(path=odb_basename + '.odb')
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]

stresses_ED = [odb.steps["Step-1"].frames[-1].fieldOutputs['S'].getSubset(region=element).values[k_gauss].data[0] for element in instance.elementSets['E-WALL'].elements for k_gauss in range(8)]
stresses_ES = [odb.steps["Step-2"].frames[-1].fieldOutputs['S'].getSubset(region=element).values[k_gauss].data[0] for element in instance.elementSets['E-WALL'].elements for k_gauss in range(8)]

data_file = open(odb_basename + '.fiber_stress_distribution.dat', 'w')
data_file.write('# Sff_ED Sff_ES\n')

for k_element in range(len(instance.elementSets['E-WALL'].elements)):
    for k_gauss in range(8):
        k_val = 8*k_element+k_gauss
        data_file.write(str(stresses_ED[k_val]) + " " + str(stresses_ES[k_val]) + "\n")

data_file.close()

odb.close()
