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
import LinearAlgebra
import Numeric

### --------------------------------------------- ### INITIALIZATION ###

odb_basename = sys.argv[1]
odb_name     = odb_basename + '.odb'
odb          = odbAccess.openOdb(path=odb_name)

step   = odb.steps['Step-1']
frames = step.frames

root_assembly   = odb.rootAssembly
instance        = root_assembly.instances['PART-1-1']

nb_dim = int(sys.argv[2])
nb_vec = nb_dim*(nb_dim+1)/2

if (len(sys.argv) == 3+nb_dim): L = [float(sys.argv[3+k_dim]) for k_dim in range(nb_dim)]
else:                           L = [1.]*nb_dim

if   (nb_dim == 2): S = [L[1], L[0]]
elif (nb_dim == 3): S = [L[1]*L[2], L[2]*L[0], L[0]*L[1]]

dummy_node_sets = [instance.nodeSets['NODES_V' + str(k_dim+1)] for k_dim in range(nb_dim)]

if   (nb_dim == 2): step_names = 'eps11', 'eps22', 'eps12'
elif (nb_dim == 3): step_names = 'eps11', 'eps22', 'eps33', 'eps12', 'eps13', 'eps23'

### -------------------------------------------------- ### STIFFNESS ###

H = Numeric.zeros((nb_vec,nb_vec), Numeric.Float)
for k_frame in range(1, len(frames)):
    frame = frames[k_frame]
    field = frame.fieldOutputs['RF']
    RF = []
    RF = [field.getSubset(region=dummy_node_sets[k_dim]).values[0].data for k_dim in range(nb_dim)]
    for k_dim in range(nb_dim):
        H[k_dim, k_frame-1] = RF[k_dim][k_dim]/S[k_dim]
    if   (nb_dim == 2):
        H[2, k_frame-1] = (RF[0][1]/S[0] + RF[1][0]/S[1])/2
    elif (nb_dim == 3):
        H[3, k_frame-1] = (RF[0][1]/S[0] + RF[1][0]/S[1])/2
        H[4, k_frame-1] = (RF[0][2]/S[0] + RF[2][0]/S[2])/2
        H[5, k_frame-1] = (RF[1][2]/S[1] + RF[2][1]/S[2])/2
print H

odb.close()

file = open(odb_basename + '_homogenized_stiffness_matrix' + '.dat', 'w')
for i in range(nb_vec):
    for j in range(nb_vec):
        file.write(str(H[i,j]) + ' ')
    file.write('\n')
file.close()

### ------------------------------------------------- ### COMPLIANCE ###

S = LinearAlgebra.inverse(H)
print S

file = open(odb_basename + '_homogenized_compliance_matrix' + '.dat', 'w')
for i in range(nb_vec):
    for j in range(nb_vec):
        file.write(str(S[i,j]) + ' ')
    file.write('\n')
file.close()

### ----------------------------------- ### ENGINEERING COEFFICIENTS ###

file = open(odb_basename + '_homogenized_engineering_coefficients' + '.dat', 'w')
engineering_coefficients = {}
if (nb_dim == 2):
    engineering_coefficients['E1' ] =       1. / S[0,0];
    engineering_coefficients['E2' ] =       1. / S[1,1];
    engineering_coefficients['N12'] = - S[0,1] / S[0,0];
    engineering_coefficients['N21'] = - S[1,0] / S[1,1];
    engineering_coefficients['G12'] =   1. / 2./ S[2,2];
    print 'E1  = ', engineering_coefficients['E1' ]
    print 'E2  = ', engineering_coefficients['E2' ]
    print 'N12 = ', engineering_coefficients['N12']
    print 'N21 = ', engineering_coefficients['N21']
    print 'G12 = ', engineering_coefficients['G12']
    file.write(str(engineering_coefficients['E1' ]) + ' ')
    file.write(str(engineering_coefficients['E2' ]) + ' ')
    file.write(str(engineering_coefficients['N12']) + ' ')
    file.write(str(engineering_coefficients['N21']) + ' ')
    file.write(str(engineering_coefficients['G12']) + ' ')
elif (nb_dim == 3):
    engineering_coefficients['E1' ] =       1. / S[0,0];
    engineering_coefficients['E2' ] =       1. / S[1,1];
    engineering_coefficients['E3' ] =       1. / S[2,2];
    engineering_coefficients['N12'] = - S[0,1] / S[0,0];
    engineering_coefficients['N21'] = - S[1,0] / S[1,1];
    engineering_coefficients['N13'] = - S[0,2] / S[0,0];
    engineering_coefficients['N31'] = - S[2,0] / S[2,2];
    engineering_coefficients['N23'] = - S[1,2] / S[1,1];
    engineering_coefficients['N32'] = - S[2,1] / S[2,2];
    engineering_coefficients['G12'] =   1. / 2./ S[3,3];
    engineering_coefficients['G13'] =   1. / 2./ S[4,4];
    engineering_coefficients['G23'] =   1. / 2./ S[5,5];
    print 'E1  = ', engineering_coefficients['E1' ]
    print 'E2  = ', engineering_coefficients['E2' ]
    print 'E3  = ', engineering_coefficients['E3' ]
    print 'N12 = ', engineering_coefficients['N12']
    print 'N21 = ', engineering_coefficients['N21']
    print 'N13 = ', engineering_coefficients['N13']
    print 'N31 = ', engineering_coefficients['N31']
    print 'N23 = ', engineering_coefficients['N23']
    print 'N32 = ', engineering_coefficients['N32']
    print 'G12 = ', engineering_coefficients['G12']
    print 'G13 = ', engineering_coefficients['G13']
    print 'G23 = ', engineering_coefficients['G23']
    file.write(str(engineering_coefficients['E1' ]) + ' ')
    file.write(str(engineering_coefficients['E2' ]) + ' ')
    file.write(str(engineering_coefficients['E3' ]) + ' ')
    file.write(str(engineering_coefficients['N12']) + ' ')
    file.write(str(engineering_coefficients['N21']) + ' ')
    file.write(str(engineering_coefficients['N13']) + ' ')
    file.write(str(engineering_coefficients['N31']) + ' ')
    file.write(str(engineering_coefficients['N23']) + ' ')
    file.write(str(engineering_coefficients['N32']) + ' ')
    file.write(str(engineering_coefficients['G12']) + ' ')
    file.write(str(engineering_coefficients['G13']) + ' ')
    file.write(str(engineering_coefficients['G23']) + ' ')
file.close()
