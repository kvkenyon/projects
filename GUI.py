import Tkinter
import vtk

class GUI:
    def __init__( self, rootWindow ):
        global I_TRUE, I_FALSE
 
        # Constants
        self.I_OK = 0
        self.I_NO_FILE = -10
 
        self.__vizType = Tkinter.IntVar()
        self.__vizDataset = Tkinter.IntVar()
 
        guiFactory = GUIFactory()
 
       
        # Create window frame
        self.__rootWindow = rootWindow
        self.__rootWindow.title( 'Isosurface Generation' )
        self.__frame = Tkinter.Frame( self.__rootWindow )
        self.__frame.pack( fill=Tkinter.BOTH, expand=1, side=Tkinter.TOP )
                  
 
        # Add VTK rendering viewport
        self.__vtkViewport = VTKRender( self.__frame )
 
 
        # Add menu bar
        menuBar = Tkinter.Menu( self.__frame )
        self.__rootWindow.config( menu=menuBar )
        self.__buildMenu( menuBar )
 
 
        # Add pseudo-status bar (from "An Introduction to Tkinter" )
        self.__statusLabel = guiFactory.newLabel( self.__frame, 'by: Allan Spale',
            {'relief':Tkinter.SUNKEN,'justify':Tkinter.LEFT, 'anchor':Tkinter.W }  )
 
        self.__statusErrorSettings = { 'background':'#ffffff',
                                       'foreground':'#000099' }
        self.__statusOKSettings = { 'background':self.__statusLabel.cget( 'background' ),
                                    'foreground':self.__statusLabel.cget( 'foreground' ) }
 
        self.__statusLabel.pack( fill=Tkinter.BOTH, side=Tkinter.BOTTOM )
 
 
        # Create dialog boxes
        self.__dialogGlobalDetail = DialogOptionVOI( self.__rootWindow, self.__vtkViewport )
        self.__dialogDatasetProps = DialogIsosurfaces( self.__rootWindow,
                self.__vtkViewport, self.__vizType.get() )
 
        # Initialize
        self.__vizType.set( self.__vtkViewport.ISO )
        self.__vizDataset.set( self.__vtkViewport.HEAD )
        self.__doSetVizType()
	def __buildMenu( self, menuMainMenu ):         
			menuFile = Tkinter.Menu( menuMainMenu, tearoff=0 )
			menuFile.add_command( label='Exit', command=self.__doMenuFileExit )
			menuMainMenu.add_cascade( label='File', menu=menuFile )
	 
			self.__menuViz = Tkinter.Menu( menuMainMenu, tearoff=0 )
			self.__menuViz.add_radiobutton( label='Head',
				value=self.__vtkViewport.HEAD, variable=self.__vizDataset,
				command=self.__doSetVizType )
			self.__menuViz.add_radiobutton( label='Feet',
				value=self.__vtkViewport.FEET, variable=self.__vizDataset,
				command=self.__doSetVizType )
			menuMainMenu.add_cascade( label='Visualization', menu=self.__menuViz )
	 
			self.__menuOptions = Tkinter.Menu( menuMainMenu, tearoff=0 )
			self.__menuOptions.add_command( label='Dataset Properties',
								 command=self.__doMenuOptionProps )
			self.__menuOptions.add_command(
				label='Global Level of Detail', command=self.__doMenuOptionDetail )
			menuMainMenu.add_cascade( label='Options', menu=self.__menuOptions )

	def __doSetVizType( self ):
        dataset = self.__vizDataset.get()
        viz = self.__vizType.get()
       
        if ( dataset == self.__vtkViewport.HEAD ):
            if ( viz == self.__vtkViewport.ISO ):
                self.__vtkViewport.showIsosurfaceHead()
 
        elif ( dataset == self.__vtkViewport.FEET ):
            if ( viz == self.__vtkViewport.ISO ):
                self.__vtkViewport.showIsosurfaceFeet()


	def __doMenuOptionProps( self ):
        self.__dialogDatasetProps.show()
 
	def __doMenuOptionDetail( self ):
        self.__dialogGlobalDetail.show()

	def __doMenuFileExit( self ):
        print "Bye"
        self.__vtkViewport.destroy()
        self.__rootWindow.destroy()       
        sys.exit( 0 )
        print "Done"

