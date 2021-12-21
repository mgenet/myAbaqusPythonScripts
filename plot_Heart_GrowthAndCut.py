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
import math

import odbAccess

###                                               ######################
### --------------------------------------------- ### initialization ###
###                                               ######################

odb_basename = sys.argv[1]

###                                              #######################
### -------------------------------------------- ### write data file ###
###                                              #######################

data_file = open(odb_basename + '.dat', 'w')
data_file.write('# t lambdag_X lambdag\n')

odb_name = odb_basename + '.odb'
odb      = odbAccess.openOdb(path=odb_name)

root_assembly  = odb.rootAssembly
instance       = root_assembly.instances[root_assembly.instances.keys()[0]]
inner_elements = [2934, 3191]
outer_elements = [2970, 3195]
#inner_elements = [2926]
#outer_elements = [2962]
#inner_elements = [2480]
#outer_elements = [2476]
#inner_elements = [2745]
#outer_elements = [2709]
#inner_elements = [2934, 2926, 2480, 2745, 3191]
#outer_elements = [2970, 2962, 2476, 2709, 3195]

for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        t = step.totalTime + frame.frameValue
        data_file.write(str(t))

        for inner_element in inner_elements:
            lambdag_X = frame.fieldOutputs['SDV4'].getSubset(region=instance.elements[inner_element]).values[0].data
            data_file.write(' ' + str(lambdag_X))

        for outer_element in outer_elements:
            lambdag_X = frame.fieldOutputs['SDV4'].getSubset(region=instance.elements[outer_element]).values[0].data
            data_file.write(' ' + str(lambdag_X))

        for inner_element in inner_elements:
            lambdag = frame.fieldOutputs['SDV5'].getSubset(region=instance.elements[inner_element]).values[0].data
            data_file.write(' ' + str(lambdag))

        for outer_element in outer_elements:
            lambdag = frame.fieldOutputs['SDV5'].getSubset(region=instance.elements[outer_element]).values[0].data
            data_file.write(' ' + str(lambdag))

        data_file.write('\n')

odb.close()

data_file.close()

###                                              #######################
### -------------------------------------------- ### write plot file ###
###                                              #######################

file = open(odb_basename + '.gnu', 'w')
file.write('''\
datafile = "''' + odb_basename + '''.dat"

set term pdf enhanced size 10,3
set output "''' + odb_basename + '''.pdf"
set xlabel "t (s)"
set multiplot layout 1,2
set ylabel "X ()"
set key right top box
''')
line = '''plot '''
for k_element in range(len(inner_elements)):
    line += '''datafile using ($1):($''' + str(2+k_element) + ''') with lines linewidth 5 title "inner (''' + str(inner_elements[k_element]) + ''')", '''
for k_element in range(len(outer_elements)):
    line += '''datafile using ($1):($''' + str(2+len(inner_elements)+k_element) + ''') with lines linewidth 5 title "outer (''' + str(outer_elements[k_element]) + ''')", '''
line = line[:-2] + '''\n'''
file.write(line)
file.write('''\
set ylabel "{/Symbol l}_g ()"
set key left top box
''')
line = '''plot '''
for k_element in range(len(inner_elements)):
    line += '''datafile using ($1):($''' + str(2+len(inner_elements)+len(outer_elements)+k_element) + ''') with lines linewidth 5 title "inner (''' + str(inner_elements[k_element]) + ''')", '''
for k_element in range(len(outer_elements)):
    line += '''datafile using ($1):($''' + str(2+2*len(inner_elements)+len(outer_elements)+k_element) + ''') with lines linewidth 5 title "outer (''' + str(outer_elements[k_element]) + ''')", '''
line = line[:-2] + '''\n'''
file.write(line)
file.write('''\
unset multiplot
''')
file.close()

###                                               ######################
### --------------------------------------------- ### exec plot file ###
###                                               ######################

os.system('cd SOL; gnuplot ' + odb_basename + '.gnu')
