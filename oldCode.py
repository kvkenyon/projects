import Tkinter
import sys
import vtk

from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor

#setup root for window
root = Tkinter.Tk()
root.title = ("Isosurfaces and Cutting Planes")
frame = Tkinter.Frame(root)
frame.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.TOP)

#create reader
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("heart.vtk")
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()
print reader.GetHeader()

isoValue = 120;

#here we either want to create a cutting plane or marching cubes or skip it just display the data
#in 3d

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
actor.GetProperty().SetColor(1,0.547237,0.319073)
actor.GetProperty().SetOpacity(.3)

#create render window and interactor 
ren = vtk.vtkRenderer()
ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial
ren.ResetCameraClippingRange()
ren.AddActor(actor)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.PolygonSmoothingOn()

#Setup interactor
iren = vtkTkRenderWindowInteractor(root,rw=renWin, width=400, height=400)
iren.Initialize()
iren.pack(side='top', fill='both', expand=1)
iren.Start()

#Init the interactor and render Start the interactor
renWin.Render()
root.mainloop()



