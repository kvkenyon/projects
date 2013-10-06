import vtk

class IsoSurfaceConfiguration:
	def __init__(self, isoValue):
		self.isoValue = isoValue;
		#Set default color
		self.color = (1,1,1)
		#Set default opacity
		self.opacity = 1.0

	def setColorR(color):
		self.color[0] = color

	def setColorG(color):
		self.color[1] = color

	def setColorB(color):
		self.color[2] = color
		
	def getColor(self):
		return self.color

	def setOpacity(opacity):
		self.opacity = opacity

	def getOpacity(self):
		return self.opacity

	def setIsoValue(isoValue):
		self.isoValue = isoValue

	def getIsoValue(self):
		return self.isoValue

	

class VisualizationApp:
	def __init__(self, fileName):
		return 0
		

	def createIsoSurface(isoValue):
		return 0

	def createCuttingPlane(coordinates):
		return 0

#create reader
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("heart.vtk")
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()

isoValue = 120;

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



