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

import sys

import numpy

from odbAccess import *

from VTK_py import *

########################################################################

class Field:
    def __init__(self,
                 ODB_name,
                 VTK_name,
                 nb_components,
                 with_local_coordinate_system=False):
        self.ODB_name                     = ODB_name
        self.VTK_name                     = VTK_name
        self.nb_components                = nb_components
        self.with_local_coordinate_system = with_local_coordinate_system

########################################################################

odb_basename = sys.argv[1]

########################################################################

node_set_names = ["N-WALL"]
elem_set_names = ["E-WALL"]

node_fields = [Field( "U",  "U", 3)]
elem_fields = [Field("LE", "LE", 6, True),\
               Field( "S",  "S", 6, True)]

move_mesh = 1

########################################################################

odb           = openOdb(path=odb_basename+".odb")
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]

if not (move_mesh):
    points = vtk.vtkPoints()
    for node_set_name in node_set_names:
        for node in instance.nodeSets[node_set_name].nodes:
            points.InsertNextPoint(node.coordinates)
    nb_nodes = points.GetNumberOfPoints()

cell_vtk_type = vtk.VTK_HEXAHEDRON
cell          = vtk.vtkHexahedron()
cell_array    = vtk.vtkCellArray()

for elem_set_name in elem_set_names:
    for elem in instance.elementSets[elem_set_name].elements:
        nodes = numpy.array(elem.connectivity)
        [cell.GetPointIds().SetId(num_node, nodes[num_node]-1) for num_node in range(len(nodes))]
        cell_array.InsertNextCell(cell)
nb_elems = cell_array.GetNumberOfCells()

num_frame = 0
for step_key in odb.steps.keys():
    #print step_key

    step = odb.steps[step_key]
    for frame in step.frames:
        #print frame.frameValue

        ugrid = vtk.vtkUnstructuredGrid()

        if (move_mesh):
            points = vtk.vtkPoints()
            field = frame.fieldOutputs["U"]
            for node_set_name in node_set_names:
                for node in instance.nodeSets[node_set_name].nodes:
                    pos = numpy.array(node.coordinates)
                    disp = numpy.array(field.values[node.label-1].data)
                    points.InsertNextPoint(pos+disp)
            nb_nodes = points.GetNumberOfPoints()

        ugrid.SetPoints(points)

        ugrid.SetCells(cell_vtk_type, cell_array)

        for node_field in node_fields:
            #print node_field.ODB_name

            field = frame.fieldOutputs[node_field.ODB_name]
            nb_nodes = points.GetNumberOfPoints()
            farray = createFloatArray(node_field.VTK_name, node_field.nb_components, nb_nodes)
            [farray.SetTuple(num_node, field.values[num_node].data) for num_node in range(nb_nodes)]
            ugrid.GetPointData().AddArray(farray)
            if (node_field.with_local_coordinate_system):
                for k_dim in range(3):
                    farray = createFloatArray(node_field.VTK_name+"_e"+str(k_dim+1), 3, nb_nodes)
                    [farray.SetTuple(num_node, field.values[num_node].localCoordSystem[k_dim]) for num_node in range(nb_nodes)]
                    ugrid.GetPointData().AddArray(farray)

        for elem_field in elem_fields:
            #print elem_field.ODB_name

            field = frame.fieldOutputs[elem_field.ODB_name]
            farray = createFloatArray(elem_field.VTK_name, elem_field.nb_components, nb_elems)
            if (elem_field.nb_components == 1):
                [farray.SetTuple(num_elem, [field.values[num_elem].data]) for num_elem in range(nb_elems)]
            else:
                [farray.SetTuple(num_elem,  field.values[num_elem].data ) for num_elem in range(nb_elems)]
            ugrid.GetCellData().AddArray(farray)
            if (elem_field.with_local_coordinate_system):
                for k_dim in range(3):
                    farray = createFloatArray(elem_field.VTK_name+"_e"+str(k_dim+1), 3, nb_nodes)
                    [farray.SetTuple(num_elem, field.values[num_elem].localCoordSystem[k_dim]) for num_elem in range(nb_elems)]
                    ugrid.GetCellData().AddArray(farray)

        writeXMLUGrid(ugrid, odb_basename+"-"+str(num_frame).zfill(3)+".vtu")

        num_frame += 1
        #exit()
