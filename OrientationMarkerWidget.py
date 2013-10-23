from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 553)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.gridlayout = QtGui.QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
 
class SimpleView(QtGui.QMainWindow):
 
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        cube = vtk.vtkCubeSource()
        cube.SetXLength(200)
        cube.SetYLength(200)
        cube.SetZLength(200)
        cube.Update()
        cm = vtk.vtkPolyDataMapper()
        cm.SetInputConnection(cube.GetOutputPort())
        ca = vtk.vtkActor()
        ca.SetMapper(cm)
        self.ren.AddActor(ca)
        self.axesActor = vtk.vtkAnnotatedCubeActor();
        self.axesActor.SetXPlusFaceText('R')
        self.axesActor.SetXMinusFaceText('L')
        self.axesActor.SetYMinusFaceText('H')
        self.axesActor.SetYPlusFaceText('F')
        self.axesActor.SetZMinusFaceText('P')
        self.axesActor.SetZPlusFaceText('A')
        self.axesActor.GetTextEdgesProperty().SetColor(1,1,0)
        self.axesActor.GetTextEdgesProperty().SetLineWidth(2)
        self.axesActor.GetCubeProperty().SetColor(0,0,1)
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(self.axesActor)
        self.axes.SetInteractor(self.iren)
        self.axes.EnabledOn()
        self.axes.InteractiveOn()
        self.ren.ResetCamera()
 
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    window = SimpleView()
    window.show()
    window.iren.Initialize() # Need this line to actually show the render inside Qt
    sys.exit(app.exec_())
