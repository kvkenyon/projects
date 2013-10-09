import os
import sys
import vtk
import Tkinter
import argparse
	

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
	def __init__(self, fileName):
		self.reader = self.createReader(fileName)
		
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
		self.renWin.SetSize(600,400)
		self.renWin.PolygonSmoothingOn()
	
	def setupInteractor(self,changeStyle=True):
		#Setup interactor
		self.iren = vtk.vtkRenderWindowInteractor()
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

	def displayPrompt():
		print "############## Basic Visualization Application #######################"
		print
		print "Directions: Select one of the following options:"
		print
		print "1 - Display the Data in 3D (No visualization technique)"
		print "2 - Create an isosurface with a user specified isovalue, color, and opacity"
		print "3 - Create a user defined cutting plane by enter x,y and z coordinates"
		print "q - To quit"
		print "Author: Kevin Kenyon"
		print "#####################################################################"

	def askUserInput():
		return input_raw("Select a number or q: ")


def main():
	#We depend on user input:
	#Parsing stuff
	
	parser = argparse.ArgumentParser()
	parser.add_argument ('-f', '--file', help="Need to give a valid file.", required="True")
	parser.add_argument('-d', '--data', help="Display the data without visualization technique.", action="store_true")
	parser.add_argument('-c', '--cut', help="a cutting plane of the data please", action="store_true")
	parser.add_argument('-x', '--x_cut', help="x-dimension of the cutting plane", default=0)
	parser.add_argument('-y', '--y_cut', help="y-dimension of the cutting plane", default=0)
	parser.add_argument('-z', '--z_cut', help="z-dimension of the cutting plane", default=0)
	parser.add_argument('-i', '--iso', help="Create isosurface", action="store_true")
	parser.add_argument('-v', '--isovalue', help="Add the isovalue for the surface", default=100)
	parser.add_argument('-r','--red', help="rgb value for isosurface", default=1)
	parser.add_argument('-b','--blue', help="rgb value for isosurface", default=1)
	parser.add_argument('-g','--green', help="rgb value for isosurface", default=1)
	parser.add_argument('-o','--opacity', help="opacity value for isosurface", default=1.0)
	parser.add_argument('-p','--prompt', help="Run the prompt version to do multiple runs", action="store_true") 
	args = parser.parse_args()

	print args
	#Create the app
	fileName = args.file 
	app = VisualizationApp(fileName)
	##Test if reader is functioning
	app.getFileHeader()

	if(args.data):
		app.displayData()
	elif args.iso:
		isoValue = float(args.isovalue)
		print "Type: " + str(type(isoValue))
		print "Isovalue: " + str(isoValue)
		#Create a configuration
		print "Red->" +str(args.red) + "Green->" + str(args.green) + "Blue->" + str(args.blue) + "Opacity->"+str(args.opacity)
		configuration = IsoSurfaceConfiguration(isoValue)
		configuration.setColorR(args.red)
		configuration.setColorG(args.green)
		configuration.setColorB(args.blue)
		configuration.setOpacity(args.opacity)
		app.createIsoSurface(configuration)
	elif args.cut:
		normal = {'x': args.x_cut, 'y': args.y_cut, 'z': args.z_cut}
		app.createCuttingPlane(normal,0)	
	elif args.prompt:
		app.displayPrompt()
		app.askUserInput()
		
	
		
if __name__ == "__main__":
	main()
	
