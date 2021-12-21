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

### ---------------------------------------------------------------- ###

odb_basename = sys.argv[1]

### ---------------------------------------------------------------- ###

datafile = open(odb_basename + '.nb_dofs.dat', 'r')
for line in datafile:
    if 'TOTAL NUMBER OF VARIABLES IN THE MODEL' in line:
        nb_dofs = line.split()[-1]
        print 'nb_dofs = ' + str(nb_dofs)
        break
datafile.close()

savefile = open(odb_basename + '.nb_dofs.dat', 'w')
savefile.write(nb_dofs)
savefile.close()
