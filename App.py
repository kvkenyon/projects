import Tkinter
import sys
import vtk

from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor

fileName = "heart.vtk"

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(fileName)
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

geometryFilter = vtk.vtkImageDataGeometryFilter()
geometryFilter.SetInputConnection(reader.GetOutputPort())
geometryFilter.Update()
mapperOutput  = geometryFilter.GetOutputPort()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(mapperOutput)
actor = vtk.vtkActor()
actor.SetMapper(mapper)

renWin = vtk.vtkRenderWindow()
ren = vtk.vtkRenderer()
renWin.AddRenderer(ren)

ren.AddActor(actor)
ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial

ren.ResetCamera()
cam = ren.GetActiveCamera()
cam.Elevation(-40)


## Generate the GUI
root = Tkinter.Tk()
root.withdraw()

# Define a quit method that exits cleanly.
def quit(obj=root):
    obj.quit()

def cuttingPlane(reader,ren,renWin,normal):
	structuredPointData = reader.GetOutput()
	center = structuredPointData.GetCenter()
	cuttingPlane = vtk.vtkPlane()
	#Set origin to the center of the data set so every slice makes contact
	cuttingPlane.SetOrigin(float(center[0]),float(center[1]),float(center[2]))
	cuttingPlane.SetNormal(float(normal[0]), float(normal[1]), float(normal[2]))
	cutter = vtk.vtkCutter()
	cutter.SetCutFunction(cuttingPlane)
	cutter.SetInputConnection(reader.GetOutputPort())
	cutter.Update()
	outputCutter = cutter.GetOutputPort()
	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputConnection(outputCutter)
	actor = vtk.vtkActor()
	actor.SetMapper(mapper)

	ren.RemoveAllViewProps()
	ren.AddActor(actor)
	ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial
	renWin.Render()

def isoSurface(reader,ren,renWin,isoValue,color,opacity):
	print color
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
	actor.GetProperty().SetColor(color[0],color[1],color[2])
	actor.GetProperty().SetOpacity(opacity)
	ren.RemoveAllViewProps()
	ren.AddActor(actor)
	ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial
	renWin.Render()

def volumeRender(reader,ren,renWin):
	#Create transfer mapping scalar value to opacity
	opacityTransferFunction = vtk.vtkPiecewiseFunction()
	opacityTransferFunction.AddPoint(1, 0.0)
	opacityTransferFunction.AddPoint(100, 0.1)
	opacityTransferFunction.AddPoint(255,1.0)

	colorTransferFunction = vtk.vtkColorTransferFunction()
	colorTransferFunction.AddRGBPoint(0.0,0.0,0.0,0.0)	
	colorTransferFunction.AddRGBPoint(64.0,1.0,0.0,0.0)	
	colorTransferFunction.AddRGBPoint(128.0,0.0,0.0,1.0)	
	colorTransferFunction.AddRGBPoint(192.0,0.0,1.0,0.0)	
	colorTransferFunction.AddRGBPoint(255.0,0.0,0.2,0.0)	

	volumeProperty = vtk.vtkVolumeProperty()
	volumeProperty.SetColor(colorTransferFunction)
	volumeProperty.SetScalarOpacity(opacityTransferFunction)
	volumeProperty.ShadeOn()
	volumeProperty.SetInterpolationTypeToLinear()

	compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
	volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
	volumeMapper.SetInputConnection(reader.GetOutputPort())

	volume = vtk.vtkVolume()
	volume.SetMapper(volumeMapper)
	volume.SetProperty(volumeProperty)

	ren.RemoveAllViewProps()

	ren.AddVolume(volume)
	ren.SetBackground(1,1,1)

	renWin.Render()

# Create the toplevel window
top = Tkinter.Toplevel(root)
top.title("Programming Assignment 1")
top.protocol("WM_DELETE_WINDOW", quit)

# Create some frames
f1 = Tkinter.Frame(top)
f2 = Tkinter.Frame(top)
f3 = Tkinter.Frame(top)

f1.pack(side="top", anchor="n", expand=1, fill="both")
f2.pack(side="bottom", anchor="s", expand="t", fill="x")
f3.pack(side="bottom", anchor="s", expand="t", fill="x")

# Create the Tk render widget, and bind the events
rw = vtkTkRenderWindowInteractor(f1, width=400, height=400, rw=renWin)
rw.pack(expand="t", fill="both")


# Display some information


isoValue = Tkinter.DoubleVar()
red = Tkinter.DoubleVar()
blue = Tkinter.DoubleVar()
green = Tkinter.DoubleVar()
opacity= Tkinter.DoubleVar()

def getColor():
	return [red.get(),green.get(),blue.get()]

w = Tkinter.Scale(f2, from_=100, to=400, variable = isoValue,orient=Tkinter.HORIZONTAL, label="Select iso value" )
w.pack(padx=0,pady=0,side=Tkinter.LEFT)

w1 = Tkinter.Scale(f2, from_=0.0, to=1.0, variable = red,orient=Tkinter.HORIZONTAL, label="Red:", resolution=0.1)
w1.pack(side=Tkinter.LEFT)

w3 = Tkinter.Scale(f2, from_=0.0, to=1.0, resolution=0.1, variable = green,orient=Tkinter.HORIZONTAL, label="Green:" )
w3.pack(side=Tkinter.LEFT)

w2 = Tkinter.Scale(f2, from_=0.0, to=1.0, resolution=0.1, variable = blue, orient=Tkinter.HORIZONTAL, label="Blue:" )
w2.pack(side=Tkinter.LEFT)

w4 = Tkinter.Scale(f2, from_=0.0, to=1.0, resolution=0.1, variable = opacity,orient=Tkinter.HORIZONTAL, label="Opacity:" )
w4.pack(side=Tkinter.LEFT)

b3 = Tkinter.Button(f2, text="Create IsoSurface", command= lambda: isoSurface(reader,ren,renWin,isoValue.get(),getColor(),opacity.get()))
b3.pack(side=Tkinter.LEFT)



#Create GUI for Cutting planes

x = Tkinter.DoubleVar()
y = Tkinter.DoubleVar()
z = Tkinter.DoubleVar()

def getNormal():
	return [x.get(),y.get(),z.get()]

cutterX = Tkinter.Scale(f3, from_=0, to=10, resolution=1, variable = x, orient=Tkinter.HORIZONTAL, label="X:" )
cutterX.pack(side=Tkinter.LEFT)
cutterY= Tkinter.Scale(f3, from_=0, to=10, resolution=1, variable = y,orient=Tkinter.HORIZONTAL, label="Y:" )
cutterY.pack(side=Tkinter.LEFT)
cutterZ= Tkinter.Scale(f3, from_=0, to=10, resolution=1, variable = z,orient=Tkinter.HORIZONTAL, label="Z:" )
cutterZ.pack(side=Tkinter.LEFT)

cuttingPlaneButton = Tkinter.Button(f3, text="Create Cutting Plane", command= lambda: cuttingPlane(reader,ren,renWin,getNormal()))
cuttingPlaneButton.pack(side=Tkinter.LEFT)


#Volume Render and Quit Buttons because they do not need any input values
b2 = Tkinter.Button(f2, text="Create Volume Render", command= lambda: volumeRender(reader,ren,renWin))
b2.pack(side=Tkinter.BOTTOM)

b1 = Tkinter.Button(f2, text="Quit", command=quit)
b1.pack()

root.update()

# Modify some bindings, use the interactor style 'switch'
iren = renWin.GetInteractor()
istyle = vtk.vtkInteractorStyleSwitch()

iren.SetInteractorStyle(istyle)
istyle.SetCurrentStyleToTrackballCamera()

axes = vtk.vtkAxesActor()
widget = vtk.vtkOrientationMarkerWidget()

widget.SetOutlineColor(0.9300,0.5700,0.1300)
widget.SetOrientationMarker(axes)
widget.SetInteractor(iren)
widget.SetViewport(0.0,0.0,0.4,0.4)
widget.SetEnabled(1)
widget.InteractiveOn()

ren.ResetCamera()

iren.Initialize()
renWin.Render()
iren.Start()

root.mainloop()

