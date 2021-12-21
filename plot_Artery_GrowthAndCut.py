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

root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]
element0      = instance.elements[0]
element1      = instance.elements[-1]

for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        t = step.totalTime + frame.frameValue
        #print t
        data_file.write(str(t))

        field = frame.fieldOutputs['SDV4']
        lambdag_X0 = field.getSubset(region=element0).values[0].data
        data_file.write(' ' + str(lambdag_X0))
        lambdag_X1 = field.getSubset(region=element1).values[0].data
        data_file.write(' ' + str(lambdag_X1))

        field = frame.fieldOutputs['SDV5']
        lambdag0 = field.getSubset(region=element0).values[0].data
        data_file.write(' ' + str(lambdag0))
        lambdag1 = field.getSubset(region=element1).values[0].data
        data_file.write(' ' + str(lambdag1))

        data_file.write('\n')

print "lambdag_min =", lambdag1
print "lambdag_max =", lambdag0

node = instance.nodes[0]
U = odb.steps[odb.steps.keys()[-1]].frames[-1].fieldOutputs['U'].getSubset(region=node).values[0].data
theta = 2 * math.atan(U[1]/(20.+U[0])) * 180./math.pi
print "theta =", theta

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
plot datafile using ($1):($2) with lines linewidth 5 title "inner",\
     datafile using ($1):($3) with lines linewidth 5 title "outer"
set ylabel "{/Symbol l}_g ()"
set key left top box
plot datafile using ($1):($4) with lines linewidth 5 title "inner",\
     datafile using ($1):($5) with lines linewidth 5 title "outer"
set key off
unset multiplot
''')
file.close()

###                                               ######################
### --------------------------------------------- ### exec plot file ###
###                                               ######################

os.system('cd SOL; gnuplot ' + odb_basename + '.gnu')
