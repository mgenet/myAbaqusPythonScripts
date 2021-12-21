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

data_file = open(odb_basename+'.txt', 'w')
data_file.write('# t LE S SDVs\n')

odb_name = odb_basename + '.odb'
odb      = odbAccess.openOdb(path=odb_name)

root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]
element       = instance.elements[0]

for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        t = step.totalTime + frame.frameValue
        #print t
        data_file.write(str(t))

        field = frame.fieldOutputs['LE']
        LE = field.getSubset(region=element).values[0].data
        #print LE
        for LEij in LE: data_file.write(' ' + str(LEij))

        field = frame.fieldOutputs['S']
        S = field.getSubset(region=element).values[0].data
        #print S
        for Sij in S: data_file.write(' ' + str(Sij))

        nb_sdv = sum(['SDV' in field_name for field_name in frame.fieldOutputs.keys()])
        #print "nb_sdv = " + str(nb_sdv)
        for i in range(1,nb_sdv+1):
            field = frame.fieldOutputs['SDV'+str(i)]
            SDV = field.getSubset(region=element).values[0].data
            #print SDV
            data_file.write(' ' + str(SDV))

        data_file.write('\n')

odb.close()

data_file.close()

###                                              #######################
### -------------------------------------------- ### write plot file ###
###                                              #######################

file = open(odb_basename+'.gnu', 'w')
file.write('''\
datafile = "'''+odb_basename+'''.txt"

set term pdf enhanced size 10,6
set output "'''+odb_basename+'''_strain.pdf"
#set key off
set xlabel "t (s)"
#set xrange [0:*]
#set yrange [0:*]
set xzeroaxis
#set yzeroaxis
set multiplot layout 2,3
set ylabel "E_{11} (%)"
plot datafile using ($1):(100*$2) smooth csplines with lines linewidth 5 notitle
set ylabel "E_{22} (%)"
plot datafile using ($1):(100*$3) smooth csplines with lines linewidth 5 notitle
set ylabel "E_{33} (%)"
plot datafile using ($1):(100*$4) smooth csplines with lines linewidth 5 notitle
set ylabel "E_{12} (%)"
plot datafile using ($1):(100*$5) smooth csplines with lines linewidth 5 notitle
set ylabel "E_{13} (%)"
plot datafile using ($1):(100*$6) smooth csplines with lines linewidth 5 notitle
set ylabel "E_{23} (%)"
plot datafile using ($1):(100*$7) smooth csplines with lines linewidth 5 notitle
unset multiplot

set term pdf enhanced size 10,6
set output "'''+odb_basename+'''_stress.pdf"
#set key off
set xlabel "t (s)"
#set xrange [0:*]
#set yrange [0:*]
set xzeroaxis
#set yzeroaxis
set multiplot layout 2,3
set ylabel "S_{11} (kPa)"
plot datafile using ($1):($8)  smooth csplines with lines linewidth 5 notitle
set ylabel "S_{22} (kPa)"
plot datafile using ($1):($9)  smooth csplines with lines linewidth 5 notitle
set ylabel "S_{33} (kPa)"
plot datafile using ($1):($10) smooth csplines with lines linewidth 5 notitle
set ylabel "S_{12} (kPa)"
plot datafile using ($1):($11) smooth csplines with lines linewidth 5 notitle
set ylabel "S_{13} (kPa)"
plot datafile using ($1):($12) smooth csplines with lines linewidth 5 notitle
set ylabel "S_{23} (kPa)"
plot datafile using ($1):($13) smooth csplines with lines linewidth 5 notitle
unset multiplot
''')
if (nb_sdv>0):
    file.write('''
set term pdf enhanced size 10,6
set output "'''+odb_basename+'''_sdv.pdf"
#set key off
set xlabel "t (s)"
#set xrange [0:*]
#set yrange [0:*]
set xzeroaxis
#set yzeroaxis
set multiplot layout ''' + ((nb_sdv==1)*('''1,1''') \
                          + (nb_sdv==2)*('''1,2''') \
                          + (nb_sdv==3)*('''1,3''') \
                          + (nb_sdv==4)*('''2,2''') \
                          + (nb_sdv==5)*('''2,3''') \
                          + (nb_sdv==6)*('''2,3''') \
                          + (nb_sdv==7)*('''3,3''') \
                          + (nb_sdv==8)*('''3,3''') \
                          + (nb_sdv==9)*('''3,3''')) + '''
''')
    for k_sdv in range(nb_sdv):
        file.write('''
set ylabel "SDV''' + str(1+k_sdv) + '''"
plot datafile using ($1):($''' + str(14+k_sdv) + ''') smooth csplines with lines linewidth 5 notitle''')
    file.write('''
unset multiplot
''')
file.close()

###                                               ######################
### --------------------------------------------- ### exec plot file ###
###                                               ######################

os.system('gnuplot '+odb_basename+'.gnu')
