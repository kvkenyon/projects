import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

#create reader
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("heart.vtk")
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

geom = vtk.vtkImageDataGeometryFilter()
geom.SetInputConnection(reader.GetOutputPort())
geom.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(geom.GetOutputPort())
mapper.Update()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.RotateY(45)


#create render window and interactor 
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(actor)
ren.SetBackground(.3,.6,.3)

renWin.Render()
iren.Start()



