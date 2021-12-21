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

import os
import sys

### ---------------------------------------------------------------- ###

odb_basename = sys.argv[1]

### ---------------------------------------------------------------- ###

total_time = 0.

datafile = open(odb_basename + '.dat', 'r')
for line in datafile:
    if 'WALLCLOCK TIME (SEC)' in line:
        total_time += float(line.split()[-1])
        print 'total_time = ' + str(total_time)
datafile.close()

savefile = open(odb_basename + '.total_time.dat', 'w')
savefile.write(str(total_time))
savefile.close()
