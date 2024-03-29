import os
import sys
import vtk
import Tkinter
from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor
	
class IsoSurfaceConfiguration:
	def __init__(self, isoValue):
		self.isoValue = isoValue;
		#Set default color
		self.color = { 'r' : 1, 'g':1, 'b':1} 
		#Set default opacity
		self.opacity = 1.0

	def setColorR(self,color):
		print "setting red"
		print
		self.color['r'] = color

	def setColorG(self,color):
		print "setting green"
		print
		self.color['g'] = color

	def setColorB(self,color):
		print "setting blue"
		print
		self.color['b'] = color
		
	def getColorR(self):
		#print "Red: " + str(self.color['r'])
		return self.color['r']

	def getColorG(self):
		return self.color['g']

	def getColorB(self):
		return self.color['b']

	def setOpacity(self,opacity):
		self.opacity = opacity

	def getOpacity(self):
		return self.opacity

	def setIsoValue(self,isoValue):
		self.isoValue = isoValue

	def getIsoValue(self):
		return self.isoValue

	

class VisualizationApp:
	def __init__(self, fileName, root):
		self.reader = self.createReader(fileName)
		self.root = root
		
	def createReader(self,fileName):
		#I dont care about different types of readers for now
		#If i get a different file then i can mod reader here or something
		reader = vtk.vtkStructuredPointsReader()
		reader.SetFileName(fileName)
		reader.ReadAllVectorsOn()
		reader.ReadAllScalarsOn()
		reader.Update()
		self.determineCenterForCuttingPlane(reader)
		return reader 

	def determineCenterForCuttingPlane(self,reader):
		structuredPointData = reader.GetOutput()
		self.center = structuredPointData.GetCenter()

	def getFileHeader(self):
		print self.reader.GetHeader()

	def displayData(self):
		geometryFilter = vtk.vtkImageDataGeometryFilter()
		geometryFilter.SetInputConnection(self.reader.GetOutputPort())
		geometryFilter.Update()
		self.outputPortForMapper = geometryFilter.GetOutputPort()
		self.createMapper(False)	
		self.createActor()
		self.finalizePipeline()

	def createIsoSurface(self,configuration):
		marchingCube = vtk.vtkMarchingCubes()
		marchingCube.SetInputConnection(self.reader.GetOutputPort())
		marchingCube.SetValue(0,configuration.getIsoValue())
		marchingCube.ComputeNormalsOn()
		self.outputPortForMapper = marchingCube.GetOutputPort()
		self.createMapper()
		self.createActor()
		self.modifyActorIso(configuration)
		self.finalizePipeline()

	def createCuttingPlane(self,normal,dimension):
		cuttingPlane = vtk.vtkPlane()
		#Set origin to the center of the data set so every slice makes contact
		cuttingPlane.SetOrigin(float(self.center[0]),float(self.center[1]),float(self.center[2]))
		cuttingPlane.SetNormal(float(normal['x']), float(normal['y']), float(normal['z']))
		self.cutter = self.createCutter(cuttingPlane)
		self.outputPortForMapper = self.cutter.GetOutputPort()
		self.createMapper(False)
		self.createActor()
		rotationDegrees = 45
		self.modifyActorForCuttingPlane(rotationDegrees)
		self.finalizePipeline()

	def createCutter(self,cuttingPlane):
		cutter = vtk.vtkCutter()
		cutter.SetCutFunction(cuttingPlane)
		cutter.SetInputConnection(self.reader.GetOutputPort())
		cutter.Update()
		return cutter

	def volumeRender(self):
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
		volumeMapper.SetInputConnection(self.reader.GetOutputPort())

		volume = vtk.vtkVolume()
		volume.SetMapper(volumeMapper)
		volume.SetProperty(volumeProperty)

		ren = vtk.vtkRenderer()
		renWin = vtk.vtkRenderWindow()
		renWin.AddRenderer(ren)

		iren = vtkTkRenderWindowInteractor(self.root, rw=renWin, width=640, height=480)
		iren.Initialize()

		ren.AddVolume(volume)
		ren.SetBackground(1,1,1)

		renWin.Render()


	def createMapper(self,turnOffScalarVisibilty=True):
		self.mapper = vtk.vtkPolyDataMapper()
		self.mapper.SetInputConnection(self.outputPortForMapper)
		if turnOffScalarVisibilty:
				self.mapper.ScalarVisibilityOff()
		self.mapper.Update()

	def createActor(self):
		self.actor = vtk.vtkActor()
		self.actor.SetMapper(self.mapper)

	def modifyActorIso(self,configuration):
		self.actor.GetProperty().SetColor(float(configuration.getColorR()), float(configuration.getColorG()),float(configuration.getColorB()))
		self.actor.GetProperty().SetOpacity(float(configuration.getOpacity()))
	
	def modifyActorForCuttingPlane(self, rotationDegrees):
		self.actor.RotateY(rotationDegrees)

	def finalizePipeline(self):
		self.createRenderWindow()
		self.setupInteractor()
		self.finalizeRenderer()
		self.start()

	def createRenderWindow(self):
		#create render window and interactor 
		self.ren = vtk.vtkRenderer()
		self.renWin = vtk.vtkRenderWindow()
		self.renWin.AddRenderer(self.ren)
		self.renWin.PolygonSmoothingOn()
	
	def setupInteractor(self,changeStyle=True):
		#Setup interactor
		self.iren = vtk.vtkTkRenderWindowInteractor()
		self.iren.SetRenderWindow(self.renWin)
		if changeStyle:
				style = vtk.vtkInteractorStyleTrackballCamera()
				self.iren.SetInteractorStyle(style)

	def finalizeRenderer(self):
		#Add actor to renderer
		self.ren.SetBackground(0.329412, 0.34902, 0.427451) #paraview blue from tutorial
		self.ren.AddActor(self.actor)
		
	def start(self):
		#Init the interactor and render Start the interactor
		self.iren.Initialize()
		self.renWin.Render()
		self.iren.Start()

def main():
	root = Tkinter.Tk()
	root.title=("Kevin Kenyon Vis App")
	frame = Tkinter.Frame(root)
	frame.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.TOP)

	app = VisualizationApp("heart.vtk", root)
	app.volumeRender()

	root.mainLoop()
	
		
if __name__ == "__main__":
	main()
	
