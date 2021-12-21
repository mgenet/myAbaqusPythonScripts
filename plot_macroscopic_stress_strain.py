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

import sys

import odbAccess

from CompMechTools.DataFile.DataFile import DataFile

from CompMechTools.Cell.Utils import *

###                                               ######################
### --------------------------------------------- ### initialization ###
###                                               ######################

cell = create_cell(sys.argv[1])
if (len(sys.argv) > 2): cell.set_mesh_parameters_from_argv(sys.argv[2:])
cell.set_bounding_box()
cell.set_faces()

odb_basename = sys.argv[1]
odb_name     = odb_basename + '.odb'
odb          = odbAccess.openOdb(path=odb_name)

step   = odb.steps['Step-1']
frames = step.frames

root_assembly   = odb.rootAssembly
instance        = root_assembly.instances['PART-1-1']

dummy_node_sets = [instance.nodeSets['NODES_V' + str(k_dim+1)] for k_dim in range(cell.nb_dim)]

if   (cell.nb_dim == 2): datafile = DataFile('SOL', 'stress_strain', ['t (s)', 'eps11 (%)', 'eps22 (%)', 'eps12 (%)', 'sig11 (MPa)', 'sig22 (MPa)', 'sig12 (MPa)'])
elif (cell.nb_dim == 3): datafile = DataFile('SOL', 'stress_strain', ['t (s)', 'eps11 (%)', 'eps22 (%)', 'eps33 (%)', 'eps12 (%)', 'eps13 (%)', 'eps23 (%)', 'sig11 (MPa)', 'sig22 (MPa)', 'sig33 (MPa)', 'sig12 (MPa)', 'sig13 (MPa)', 'sig23 (MPa)'])

###                            #########################################
### -------------------------- ### read odf file and write data file ###
###                            #########################################

for frame in frames:
    t = frame.frameValue

    field = frame.fieldOutputs['U']
    U = [field.getSubset(region=dummy_node_sets[k_dim]).values[0].data for k_dim in range(cell.nb_dim)]
    eps = [U[k_dim][k_dim]/(cell.BB.Pmax[k_dim]-cell.BB.Pmin[k_dim]) for k_dim in range(cell.nb_dim)]
    if   (cell.nb_dim == 2):
        eps.append((U[0][1]/(cell.BB.Pmax[0]-cell.BB.Pmin[0])+U[1][0]/(cell.BB.Pmax[1]-cell.BB.Pmin[1]))/2)
    elif (cell.nb_dim == 3):
        eps.append((U[0][1]/(cell.BB.Pmax[0]-cell.BB.Pmin[0])+U[1][0]/(cell.BB.Pmax[1]-cell.BB.Pmin[1]))/2)
        eps.append((U[0][2]/(cell.BB.Pmax[0]-cell.BB.Pmin[0])+U[2][0]/(cell.BB.Pmax[2]-cell.BB.Pmin[2]))/2)
        eps.append((U[1][2]/(cell.BB.Pmax[1]-cell.BB.Pmin[1])+U[2][1]/(cell.BB.Pmax[2]-cell.BB.Pmin[2]))/2)

    field = frame.fieldOutputs['RF']
    RF = [field.getSubset(region=dummy_node_sets[k_dim]).values[0].data for k_dim in range(cell.nb_dim)]
    sig = [RF[k_dim][k_dim]/cell.S[k_dim] for k_dim in range(cell.nb_dim)]
    if   (cell.nb_dim == 2):
        sig.append((RF[0][1]/cell.S[0]+RF[1][0]/cell.S[1])/2)
    elif (cell.nb_dim == 3):
        sig.append((RF[0][1]/cell.S[0]+RF[1][0]/cell.S[1])/2)
        sig.append((RF[0][2]/cell.S[0]+RF[2][0]/cell.S[2])/2)
        sig.append((RF[1][2]/cell.S[1]+RF[2][1]/cell.S[2])/2)

    datafile.write_point([t] + eps + sig)

odb.close()

###                                              #######################
### -------------------------------------------- ### write plot file ###
###                                              #######################

file = open(datafile.get_plot_name(), 'w')
if (cell.nb_dim == 2):
    file.write('''\
set term pdf enhanced

datafile = "''' + datafile.name + '''".".dat"

set output "stress_strain.pdf"

set key off

set xlabel '{/Symbol e} (%)'
set ylabel '{/Symbol s} (MPa)'

set xrange [0:*]
set yrange [0:*]

plot datafile using (100*$2):($5) with lines linewidth 5
#plot datafile using (100*$3):($6) with lines linewidth 5
#plot datafile using (100*$4):($7) with lines linewidth 5

set output "time.pdf"

set multiplot layout 2, 1

set key left top

set xlabel 't (s)'
set ylabel '{/Symbol s} (MPa)'

set xrange [0:*]
set yrange [0:*]

plot datafile using ($1):($5) with lines linetype 1 linewidth 5 title "sig11",\\
     datafile using ($1):($6) with lines linetype 3 linewidth 4 title "sig22",\\
     datafile using ($1):($7) with lines linetype 5 linewidth 3 title "sig12"

set key left top

set xlabel 't (s)'
set ylabel '{/Symbol e} (%)'

set xrange [0:*]
set yrange [*:*]

plot datafile using ($1):(100*$2) with lines linetype 1 linewidth 5 title "eps11",\\
     datafile using ($1):(100*$3) with lines linetype 3 linewidth 4 title "eps22",\\
     datafile using ($1):(100*$4) with lines linetype 5 linewidth 3 title "eps12"

unset multiplot
''')
elif (cell.nb_dim == 3):
    file.write('''\
set term pdf enhanced

datafile = "''' + datafile.name + '''".".dat"

set output "stress_strain.pdf"

set key off

set xlabel '{/Symbol e} (%)'
set ylabel '{/Symbol s} (MPa)'

set xrange [0:*]
set yrange [0:*]

plot datafile using (100*$2):($8) with lines linewidth 5

set output "time.pdf"

set multiplot layout 2, 1

set key left top

set xlabel 't (s)'
set ylabel '{/Symbol s} (MPa)'

set xrange [0:*]
set yrange [0:*]

plot datafile using ($1):($8 ) with lines linewidth 6 title "sig11",\\
     datafile using ($1):($9 ) with lines linewidth 5 title "sig22",\\
     datafile using ($1):($10) with lines linewidth 4 title "sig33",\\
     datafile using ($1):($11) with lines linewidth 3 title "sig12",\\
     datafile using ($1):($12) with lines linewidth 2 title "sig13",\\
     datafile using ($1):($13) with lines linewidth 1 title "sig23"

set key left top

set xlabel 't (s)'
set ylabel '{/Symbol e} (%)'

set xrange [0:*]
set yrange [*:*]

plot datafile using ($1):(100*$2) with lines linewidth 6 title "eps11",\\
     datafile using ($1):(100*$3) with lines linewidth 5 title "eps22",\\
     datafile using ($1):(100*$4) with lines linewidth 4 title "eps33",\\
     datafile using ($1):(100*$5) with lines linewidth 3 title "eps12",\\
     datafile using ($1):(100*$6) with lines linewidth 2 title "eps13",\\
     datafile using ($1):(100*$7) with lines linewidth 1 title "eps23"

unset multiplot
''')
file.close()

###                                               ######################
### --------------------------------------------- ### exec plot file ###
###                                               ######################

datafile.exec_plot_file()
