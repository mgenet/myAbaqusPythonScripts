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

import numpy
import sys
import vtk

import odbAccess

import myVTKPythonLibrary as myvtk

########################################################################

class Field:
    def __init__(self, ODB_name, VTK_name, nb_components):
        self.ODB_name      = ODB_name
        self.VTK_name      = VTK_name
        self.nb_components = nb_components

########################################################################

odb_basename = sys.argv[1]

########################################################################

node_set_names = ["HEART-1_ALL-SOLIDS"]
elem_set_names = ["HEART-1_ALL-SOLIDS"]

#elem_id_names = ['HEART-1_ARCH']
elem_id_names = ['HEART-1_ARCH', 'HEART-1_ATRIA', 'HEART-1_PULM', 'HEART-1_VENA-CAVA', 'HEART-1_VENTRICLES']

fiber_names = ['BASE', 'VENA-CAVA', 'PULM', 'ARCH', 'APP']

point_fields = [Field("U", "U", 3)]
cell_fields  = [Field(  "LE",        "LE", 6),\
                Field(   "S",         "S", 6),\
                Field("SDV1",        "Je", 1),\
                Field("SDV3",         "l", 1),\
                Field("SDV5", "lambdag_X", 1),\
                Field("SDV7",   "lambdag", 1)]

########################################################################

odb           = odbAccess.openOdb(path=odb_basename+".odb")
root_assembly = odb.rootAssembly
instance      = root_assembly.instances[root_assembly.instances.keys()[0]]

points = vtk.vtkPoints()

nb_nodes = 0
for node_set_name in node_set_names:
    for node in instance.nodeSets[node_set_name].nodes:
        nb_nodes += 1

        points.InsertNextPoint(node.coordinates)

cell_vtk_type = vtk.VTK_TETRA
cell          = vtk.vtkTetra()
cell_array    = vtk.vtkCellArray()

farray_elem_id = myvtk.createFloatArray("elem_id", 1)

elem_id_labels = [[elem.label for elem in instance.elementSets[elem_id_name].elements] for elem_id_name in elem_id_names]

farray_eF = myvtk.createFloatArray("eF", 3)
farray_eS = myvtk.createFloatArray("eS", 3)
farray_eN = myvtk.createFloatArray("eN", 3)

fiber_lines = []
for fiber_name in fiber_names:
    fiber_lines += open(fiber_name+'-DF.inp').readlines()

nb_elements = 0
for elem_set_name in elem_set_names:
    for element in instance.elementSets[elem_set_name].elements:
        nb_elements += 1

        nodes = numpy.array(element.connectivity)
        [cell.GetPointIds().SetId(num_node, nodes[num_node]-1) for num_node in range(len(nodes))]
        cell_array.InsertNextCell(cell)

        elem_id = 0
        for k_elem_id in range(len(elem_id_names)):
            if (element.label in elem_id_labels[k_elem_id]):
                elem_id = k_elem_id+1
                break
        farray_elem_id.InsertNextTuple([elem_id])

        fiber_line = fiber_lines[nb_elements-1].split(', ')
        eF = [float(item) for item in fiber_line[1:4]]
        eS = [float(item) for item in fiber_line[4:7]]
        eN = numpy.cross(eF,eS)
        farray_eF.InsertNextTuple(eF)
        farray_eS.InsertNextTuple(eS)
        farray_eN.InsertNextTuple(eN)

num_frame = 0
for step_key in odb.steps.keys():
    step = odb.steps[step_key]
    for frame in step.frames:
        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.SetPoints(points)
        ugrid.SetCells(cell_vtk_type, cell_array)
        ugrid.GetCellData().AddArray(farray_elem_id)
        ugrid.GetCellData().AddArray(farray_eF)
        ugrid.GetCellData().AddArray(farray_eS)
        ugrid.GetCellData().AddArray(farray_eN)

        for point_field in point_fields:
            field = frame.fieldOutputs[point_field.ODB_name]
            farray = myvtk.createFloatArray(point_field.VTK_name, point_field.nb_components, nb_nodes)
            [farray.SetTuple(num_node, field.values[num_node].data) for num_node in range(nb_nodes)]
            ugrid.GetPointData().AddArray(farray)

        for cell_field in cell_fields:
            field = frame.fieldOutputs[cell_field.ODB_name]
            farray = myvtk.createFloatArray(cell_field.VTK_name, cell_field.nb_components, nb_elements)
            if (cell_field.nb_components == 1):
                [farray.SetTuple(num_element, [field.values[num_element].data]) for num_element in range(nb_elements)]
            else:
                [farray.SetTuple(num_element,  field.values[num_element].data ) for num_element in range(nb_elements)]
            ugrid.GetCellData().AddArray(farray)

        myvtk.writeUGrid(ugrid, odb_basename+"-"+str(num_frame).zfill(3)+".vtu")

        num_frame += 1
