"""
This class is more like a factory than an instantiatable class.  It helps
create Tkinter widgets without a lot of repetitive configuration.
"""
class GUIFactory:
    global I_TRUE, I_FALSE
    
    def __init__( self ):
        self.__dictStandardGridSettings = { 'padx':5, 'pady':5, 'sticky':Tkinter.SW}
        self.__defaultFont = tkFont.Font( size=11 )


    def newLabel( self, rootPanel, labelText, dictExtraConfig ):
        l = Tkinter.Label( rootPanel, font=self.__defaultFont, text=labelText )

        if ( self.__isConfigEmpty( dictExtraConfig ) == I_FALSE ):
            l.config( dictExtraConfig )
            
        return l


    def newEntry( self, rootPanel, fieldIdentifier, dictExtraConfig ):
        e = Tkinter.Entry( rootPanel, font=self.__defaultFont, text=fieldIdentifier )

        if ( self.__isConfigEmpty( dictExtraConfig ) == I_FALSE ):
            e.config( dictExtraConfig )

        return e


    def newButton( self, rootPanel, buttonText, buttonCommand, dictExtraConfig ):
        b = Tkinter.Button( rootPanel, font=self.__defaultFont, text=buttonText,
                            command=buttonCommand )
        
        if ( self.__isConfigEmpty( dictExtraConfig ) == I_FALSE ):
            b.config( dictExtraConfig )

        return b


    def newCheckbox( self, rootPanel, checkText, checkCommand, dictExtraConfig ):
        c = Tkinter.Checkbutton( rootPanel, font=self.__defaultFont, text=checkText,
                                 command=checkCommand, indicatoron=I_FALSE )
        
        if ( self.__isConfigEmpty( dictExtraConfig ) == I_FALSE ):
            c.config( dictExtraConfig )

        return c


    def newRadiobutton( self, rootPanel, radioText, radioCommand, sharedVariable,
                        radioValue, dictExtraConfig ):
        r = Tkinter.Radiobutton( rootPanel, font=self.__defaultFont, text=radioText,
                                 command=radioCommand, variable=sharedVariable,
                                 value=radioValue, indicatoron=I_FALSE )

        if ( self.__isConfigEmpty( dictExtraConfig ) == I_FALSE ):
            r.config( dictExtraConfig )

        return r


    def newSlider( self, rootPanel, sliderCommand, valueStart, valueEnd,
                   dictExtraConfig ):

        dictExtraConfig[ 'from' ] = valueStart
        dictExtraConfig[ 'to' ] = valueEnd
        dictExtraConfig[ 'orient' ] = Tkinter.HORIZONTAL
        dictExtraConfig[ 'showvalue' ] = I_FALSE

        s = Tkinter.Scale( rootPanel )
        s.config( dictExtraConfig )
        
        s.bind( '<B1-Motion>', sliderCommand )
        s.bind( '<B2-Motion>', sliderCommand )
        s.bind( '<Button-1>', sliderCommand )
        s.bind( '<Button-2>', sliderCommand )
        s.bind( '<ButtonRelease-1>', sliderCommand )
        s.bind( '<ButtonRelease-2>', sliderCommand )
        
        return s
    

    def newListbox( self, rootPanel, dictExtraConfig ):
        dictExtraConfig[ 'selectmode' ] = Tkinter.SINGLE

        l = Tkinter.Listbox( rootPanel, font=self.__defaultFont )
        l.config( dictExtraConfig )

        return l
    
        
    def packItem( self, object, gridSettings ):
        items = self.__dictStandardGridSettings.keys()

        for x in items:
            gridSettings[ x ] = self.__dictStandardGridSettings[ x ]

        object.grid( gridSettings )


    def __isConfigEmpty( self, dictConfig ):
        if ( dictConfig == None ):
            return I_TRUE
        elif ( len( dictConfig ) > 0 ):
            return I_FALSE
        else:
            return I_TRUE



"""
This is a composited widget made from Tkinter.Scale and Tkinter.Label.
Class methods are available to allow some level of customizability.
"""
class SliderWithValue:
    global I_TRUE, I_FALSE
    
    def __init__( self, rootPanel, startValue, endValue ):
        guiFactory = GUIFactory()
        #self.count = 0
        self.__root = rootPanel
        self.__frame = Tkinter.Frame( self.__root )
                                 
        self.__label = guiFactory.newLabel( self.__frame, '',
                                            { 'padx':5, 'pady':5,
                                              'anchor':Tkinter.SW,
                                              'width':3,
                                              'justify':Tkinter.RIGHT} )
        self.__label.grid(row=0, rowspan=1, column=0, columnspan=3,
                          sticky=Tkinter.NW )

        filler = guiFactory.newLabel( self.__frame, ' ', None )
        filler.grid( row=0, rowspan=1, column=3, columnspan=1 )
                            
        self.__slider = guiFactory.newSlider( self.__frame, self.__updateLabel,
                                              startValue, endValue,
                                              {} )
        self.__slider.grid( row=0, rowspan=1, column=4, columnspan=3,
                            sticky=Tkinter.NE)
        self.__slider.set( startValue )

        self.__modified = I_FALSE
        self.__sliderValue = startValue
        
        self.__updateLabel()


    def addSliderCommandBinding( self, callback ):
        self.__slider.bind( '<B1-Motion>', callback )
        self.__slider.bind( '<B2-Motion>', callback )
        self.__slider.bind( '<Button-1>', callback )
        self.__slider.bind( '<Button-2>', callback )
        self.__slider.bind( '<ButtonRelease-1>', callback )
        self.__slider.bind( '<ButtonRelease-2>', callback )
        

    def configureScale( self, dictConfiguration ):
        self.__slider.config( dictConfiguration )


    def setScaleValue( self, value ):
        self.__slider.set( value )
        self.__updateLabel()

    
    def reset( self ):
        value = self.__slider.cget( 'from' )
        self.__slider.set( value )
        self.__updateLabel()
        self.__modified = I_FALSE

    def configureLabel( self, dictConfiguration ):
        self.__label.config( dictConfiguration )


    def getWidget( self ):
        return self.__frame


    def getValue( self ):
        return self.__slider.get()

    def getValue2( self ):
        return int( self.__label.cget( 'text' ) )


    def getValue3( self ):
        return self.__sliderValue



    def __updateLabel( self, *unusedArgument ):
        #print self.count, self.__valueLabel
        #self.count = self.count+1
        #self.__label = self.__slider.get()
        self.__label.config( text=self.__slider.get() )
        self.__modified = I_TRUE
        self.__sliderValue = self.__slider.get()


    def getModifiedStatus():
        return self.__modified


"""
This is a class that creates a dialog.  All dialog boxes will extend this class.
"""
class Dialog:
    global I_TRUE, I_FALSE

    
    def __init__( self, topWindow, dialogTitle, useStatusBarFlag ):
        self.__firstTime = I_TRUE
        self.__buildDialog( topWindow, dialogTitle, useStatusBarFlag )

        self.config = {}
        self.config[ 'text' ] = ''
        self.config[ 'foreground' ] = ''
        self.config[ 'background' ] = ''



    def __buildDialog( self, root, title, statusBarFlag ):
        self.__rootWindow = root
        self.__title = title
        self.__statusBarFlag = statusBarFlag
        self.__root = Tkinter.Toplevel( self.__rootWindow )
        self.__root.title( title )
        #self.__root.resizable( 0,0 )
        self.dialog = Tkinter.Frame( self.__root )
        self.dialog.pack()
        

        # constants
        self.B_USE_ERROR_COLOR = I_TRUE
        self.B_NO_ERROR_COLOR = I_FALSE


        """if ( self.__statusBarFlag == I_TRUE ):
            self.__statusBar = Tkinter.Label( self.__root, relief=Tkinter.SUNKEN,
                                              text=' ', justify=Tkinter.LEFT,
                                              anchor=Tkinter.W )
            self.__statusBar.pack()
            self.__statusOriginalBGColor = self.__statusBar.cget( 'background' )
            self.__statusOriginalFGColor = self.__statusBar.cget( 'foreground' )
        """
        self.hide()


    def rebuildDialog( self, newRoot ):
        self.__rootWindow = newRoot
        self.__buildDialog( newRoot, self.__title, self.__statusBarFlag )

        
    def show( self ):
        # modal dialog settings...adopted from "An Introduction to Tkinter"

        if ( self.__firstTime == I_TRUE ):
            #self.__root.transient( self.__rootWindow )
            self.__firstTime = I_FALSE

        self.__root.deiconify()            
        #self.__root.grab_set() #events sent to this dialog
        #self.__root.focus_set()
        #self.__root.wait_window( self.__root )


    def destroy( self ):
        #self.__root.grab_release()
        self.__root.destroy()


    def hide( self ):
        #self.__root.grab_release()
        #self.__root.withdraw()
        self.__root.iconify()


    def setStatusBarMessage( self, useErrorColorFlag, statusText ):
        if ( self.__statusBarFlag == I_TRUE ):
            self.config[ 'text' ] = statusText

            if ( useErrorColorFlag == I_TRUE ):
                self.config[ 'foreground' ] = '#0000AA'
                self.config[ 'background' ] = '#FFFFFF'
                
            else:
                self.config[ 'foreground' ] = self.__statusOriginalFGColor
                self.config[ 'background' ] = self.__statusOriginalBGColor
    
            self.__statusBar.config( self.config )


    def configStatusBar( self, dictConfiguration ):
        self.__statusBar.config( dictConfiguration )
