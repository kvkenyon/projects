import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

#create reader
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("heart.vtk")
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

isoValue = 100;

marchingCube = vtk.vtkMarchingCubes()
marchingCube.SetInputConnection(reader.GetOutputPort())
marchingCube.SetValue(0,isoValue)
marchingCube.ComputeNormalsOn()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(marchingCube.GetOutputPort())
mapper.ScalarVisibilityOff()
mapper.Update()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1,1,1)
actor.GetProperty().SetOpacity(.6)

#create render window and interactor 
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600,400)
renWin.PolygonSmoothingOn()

#Setup interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

#Add actor to renderer
ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial
ren.AddActor(actor)


#Init the interactor and render Start the interactor
iren.Initialize()
renWin.Render()
iren.Start()



