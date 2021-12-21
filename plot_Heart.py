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

import odbAccess

###                                               ######################
### --------------------------------------------- ### initialization ###
###                                               ######################

odb_basename = sys.argv[1]

###                                              #######################
### -------------------------------------------- ### write data file ###
###                                              #######################

data_file = open(odb_basename + '.txt', 'w')
data_file.write('# t V P\n')

odb_name = odb_basename + '.odb'
odb      = odbAccess.openOdb(path=odb_name)

deltat = 1.
current = 0

for step_key in odb.steps.keys():
    #print 'step_key =', step_key
    step = odb.steps[step_key]

    cvol_points = step.historyRegions[step.historyRegions.keys()[0]].historyOutputs['CVOL'].data
    pcav_points = step.historyRegions[step.historyRegions.keys()[0]].historyOutputs['PCAV'].data
    if (cvol_points == None) or (pcav_points == None): continue

    assert (len(cvol_points) == len(pcav_points)), 'Lengths do not match. Aborting.'

    for k_point in range(len(cvol_points)):
        cvol_point = cvol_points[k_point]
        pcav_point = pcav_points[k_point]
        assert (cvol_point[0] == pcav_point[0]), 'Time steps do not match. Aborting.'

        t = step.totalTime + cvol_point[0]
        #print 't =', t

        cvol = cvol_point[1]
        pcav = pcav_point[1]
        #print 'cvol =', cvol
        #print 'pcav =', pcav

        data_file.write(str(t) + ' ' + str(cvol) + ' ' + str(pcav) + '\n')

        if (k_point < len(cvol_points)-1) and (int(t)-current == deltat):
            current = int(t)
            data_file.write('\n' + str(t) + ' ' + str(cvol) + ' ' + str(pcav) + '\n')

    #data_file.write('\n\n')

odb.close()

data_file.close()

###                                              #######################
### -------------------------------------------- ### write plot file ###
###                                              #######################

file = open(odb_basename + '.gnu', 'w')
file.write('''\
datafile = "''' + odb_basename + '''.txt"

set term pdf enhanced

set output "''' + odb_basename + '''_V.pdf"
set key off
set xlabel "t (s)"
set ylabel "V (ml)"
set yrange [0:*]
plot datafile using ($1):($2)/1e3 with lines linewidth 5 notitle

set output "''' + odb_basename + '''_P.pdf"
set key off
set xlabel "t (s)"
set ylabel "P (mmHg)"
set yrange [0:*]
plot datafile using ($1):($3)/0.133322 with lines linewidth 5 notitle

set output "''' + odb_basename + '''_PV.pdf"
set key off
set xlabel "V (ml)"
set ylabel "P (mmHg)"
set xrange [0:*]
set yrange [0:*]
plot datafile using ($2)/1e3:($3)/0.133322 with lines linewidth 5 notitle
''')
file.close()

###                                               ######################
### --------------------------------------------- ### exec plot file ###
###                                               ######################

os.system('gnuplot '+odb_basename+'.gnu')
