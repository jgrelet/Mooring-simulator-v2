# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mooring simulator PyQt application."""

import sys
from functools import partial
from math import floor
from os import startfile, path
from pathlib import Path
import argparse
import logging
import toml

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QWidget,
    QLabel,
    QMainWindow,
    QMenu,
    QSpinBox,
    QToolBar,
    QStyleFactory,
    QStyle,
    QFileDialog,
    QDockWidget,
    QSplashScreen,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QPushButton,
    QDialogButtonBox,
    QVBoxLayout,
)
import qrc_resources
from libraryWidget import WidgetLibrary

VERSION = "1.2.1.0"


class MainWindow(QMainWindow, QObject):
    """Main Window."""

    # defined a signal named trigger as class attribute
    trigger = pyqtSignal()

    def __init__(self, cfg, library_file_name='',
                 file_name=''):
        """In the class initializer .__init__(), you first call the parent class
        QMainWindow initializer using super(). Then you set the title of the window 
        using .setWindowTitle() and resize the window using .resize()."""
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mooring simulator v2.0")
        self.screen_width = cfg['global']['screen_width']
        self.screen_height = cfg['global']['screen_height']
        self.resize(self.screen_width, self.screen_height)
        self.cfg = cfg
        self.fileName = file_name
        self.libraryFileName = library_file_name

        # The window’s central widget is a QLabel object that you’ll use to show
        # messages in response to certain user actions. These messages will display
        # at the center of the window. To do this, you call .setAlignment() on the
        # QLabel object with a couple of alignment flags.
        self.centralWidget = QLabel(
            "Hello, welcome inside Mooring simulator, enjoy!")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        # Note that you call ._createActions() before you call ._createMenuBar() and
        # ._createToolBars() because you’ll be using these actions on your menus and
        # toolbars.
        self._createActions()
        self._createMenuBar()
        self._createToolBars()

        # Uncomment the call to ._createContextMenu() below to create a context
        # menu using menu policies. To test this out, you also need to
        # comment .contextMenuEvent() and uncomment ._createContextMenu()

        # self._createContextMenu()
        self._connectActions()
        self._createStatusBar()

        # need to be modify because the path of the library is defined in the config file now
        # if library = args.lib not empty, load library directly
        if self.libraryFileName:
            self.loadLibrary()

    def _createMenuBar(self):
        """In a PyQt main window–style application, QMainWindow provides an empty 
        QMenuBar object by default. To get access to this menu bar, you need to 
        call .menuBar() on your QMainWindow object. This method will return an 
        empty menu bar. The parent for this menu bar will be your main window object."""

        # This is the preferred way of creating a menu bar in PyQt. Here, the menuBar
        # variable will hold an empty menu bar, which will be your main window’s menu bar.
        menuBar = self.menuBar()

        # File menu
        # If you use the first option, then you need to create your custom QMenu objects
        # first. To do that, you can use one of the following constructors:
        #   QMenu(parent)
        #   QMenu(title, parent)
        # In both cases, parent is the QWidget that will hold the ownership of the QMenu
        # object. You’ll typically set parent to the window in which you’ll use the menu.
        # In the second constructor, title will hold a string with a text that describes
        # the menu option.

        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        # Creating menus using a title
        self.openRecentMenu = fileMenu.addMenu("Open Recent")
        # You can add actions to a QMenu object using .addAction(). This method has
        # several variations. Most of them are thought to create actions on the fly.
        # We use a variation of .addAction() that QMenu inherits from QWidget:
        # QWidget.addAction(action)
        # The argument action represents the QAction object that you want to add to
        # a given QWidget object. With this variation of .addAction(), you can create
        # your actions beforehand and then add them to your menus as needed.
        fileMenu.addAction(self.saveAction)
        # Separator
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        editMenu.setDisabled(True)
        # Edit separator
        editMenu.addSeparator()
        editMenu.addAction(self.zoomInAction)
        editMenu.addAction(self.zoomOutAction)

        # Library menu
        libraryMenu = menuBar.addMenu("&Library")
        libraryMenu.addAction(self.showLibraryAction)
        libraryMenu.addAction(self.loadLibraryAction)
        libraryMenu.addAction(self.refreshLibraryAction)
        libraryMenu.addAction(self.openExcelLibraryAction)

        # Configuration menu
        configurationMenu = menuBar.addMenu("&Configuration")
        configurationMenu.addAction(self.globalConfigurationAction)
        configurationMenu.addAction(self.setenvConfigurationAction)

        # Simulate menu
        simulateMenu = menuBar.addMenu("&Simulate")
        simulateMenu.addAction(self.startSimulateAction)
        simulateMenu.addAction(self.generateReportAction)
        simulateMenu.setDisabled(True)

        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def _createToolBars(self):
        # A toolbar is a movable panel that holds buttons and other widgets to provide
        # fast access to the most common options of a GUI application. Toolbar buttons
        # can display icons, text, or both to represent the task that they perform.
        # The base class for toolbars in PyQt is QToolBar. This class will allow you to
        # create custom toolbars for your GUI applications.

        # Create File toolbar using a title
        fileToolBar = self.addToolBar("File")
        fileToolBar.setMovable(False)
        fileToolBar.addAction(self.newAction)
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAction)

        # Create Edit toolbar using a QToolBar object
        self.editToolBar = QToolBar("Edit", self)
        # inserts a QToolBar object (toolbar) into the specified toolbar area (area).
        # self.addToolBar(Qt.LeftToolBarArea, editToolBar)
        self.addToolBar(self.editToolBar)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.zoomInAction)
        self.editToolBar.addAction(self.zoomOutAction)
        self.editToolBar.setDisabled(True)

        # Library toolbar
        libraryToolBar = QToolBar("Edit", self)
        self.addToolBar(libraryToolBar)
        libraryToolBar.addAction(self.showLibraryAction)
        libraryToolBar.addAction(self.loadLibraryAction)
        libraryToolBar.addAction(self.refreshLibraryAction)
        libraryToolBar.addAction(self.openExcelLibraryAction)

        # Adding Widgets to a Toolbar
        # First import the spin box class. Then create a QSpinBox object, set its
        # focusPolicy to Qt.NoFocus, and finally add it to the library toolbar.
        # self.fontSizeSpinBox = QSpinBox()
        # self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        # libraryToolBar.addWidget(self.fontSizeSpinBox)

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        # Temporary message
        self.statusbar.showMessage("Ready", 3000)
        # Permanent widget
        self.wcLabel = QLabel(f"{self.getWordCount()} Words")
        self.statusbar.addPermanentWidget(self.wcLabel)

    def _createActions(self):
        # File actions
        self.newAction = QAction(self)
        self.newAction.setText("&New mooring")
        self.newAction.setIcon(QIcon(self.style().standardIcon(getattr(QStyle,
                                                                       "SP_FileDialogNewFolder"))))
        self.openAction = QAction(
            QIcon(self.style().standardIcon(
                getattr(QStyle, "SP_DialogOpenButton"))),
            "&Open mooring", self)
        self.saveAction = QAction(
            QIcon(self.style().standardIcon(
                getattr(QStyle, "SP_DialogSaveButton"))),
            "&Save mooring", self)
        self.exitAction = QAction("&Exit", self)
        # String-based key sequences
        self.newAction.setShortcut("Ctrl+N")
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")
        # Help tips
        newTip = "Design a new mooring"
        self.newAction.setStatusTip(newTip)
        self.newAction.setToolTip(newTip)
        self.newAction.setWhatsThis("Create a new and empty mooring")

        # Edit actions
        self.copyAction = QAction(QIcon(":edit-copy.png"), "&Copy", self)
        self.pasteAction = QAction(QIcon(":edit-paste.png"), "&Paste", self)
        self.cutAction = QAction(QIcon(":edit-cut.png"), "C&ut", self)
        self.zoomInAction = QAction(QIcon(":zoom-in.png"), "Zoom in", self)
        self.zoomOutAction = QAction(QIcon(":zoom-out.png"), "Zoom out", self)
        # Standard key sequence
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.cutAction.setShortcut(QKeySequence.Cut)

        # Library actions
        self.showLibraryAction = QAction(
            QIcon(":library-show.png"), "&Show library", self)
        self.loadLibraryAction = QAction(
            QIcon(":library-load-2.png"), "&Load new library", self)
        self.refreshLibraryAction = QAction(
            QIcon(":refresh.png"), "&Refresh library", self)
        self.openExcelLibraryAction = QAction(
            QIcon(":spreadsheet.png"), "&Open Excel library", self)
        # Standard key sequence
        # self.showLibraryAction.setShortcut(QKeySequence.Copy)
        # self.loadLibraryAction.setShortcut(QKeySequence.Paste)

        # Configuration actions
        self.globalConfigurationAction = QAction(
            "Set global configuration", self)
        self.setenvConfigurationAction = QAction(
            "Set environnemental conditions", self, checkable=True)
        

        # Simulate actions
        self.startSimulateAction = QAction(
            QIcon(":play.png"), "Start simulation", self)
        self.generateReportAction = QAction("Generate report", self)

        # Help actions
        self.helpContentAction = QAction("&Help Content...", self)
        self.aboutAction = QAction("&About...", self)

        # Status bar actions
        # not well implemented
        # self.centralWidgetAction = QAction(self.centralWidget)
        # self.centralWidget.addAction(self.centralWidgetAction)
        self.trigger.connect(self.handle_trigger)

    # Uncomment this method to create a context menu using menu policies
    # def _createContextMenu(self):
    #     # Setting contextMenuPolicy
    #     self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
    #     # Populating the widget with actions
    #     self.centralWidget.addAction(self.newAction)
    #     self.centralWidget.addAction(self.openAction)
    #     self.centralWidget.addAction(self.saveAction)
    #     self.centralWidget.addAction(self.copyAction)
    #     self.centralWidget.addAction(self.pasteAction)
    #     self.centralWidget.addAction(self.cutAction)

    def contextMenuEvent(self, event):
        # Context menu
        menu = QMenu(self.centralWidget)
        # Populating the menu with actions
        menu.addAction(self.newAction)
        menu.addAction(self.openAction)
        menu.addAction(self.saveAction)
        # Separator
        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        menu.addAction(self.showLibrary)
        menu.addAction(self.pickLibrary)
        # Launching the menu
        menu.exec(event.globalPos())

    def _connectActions(self):
        """Connecting Signals and Slots in Menus and Toolbars
        In PyQt, you use signals and slots to provide functionality to your GUI 
        applications. PyQt widgets emit signals every time an event such as a mouse 
        click, a keypress, or a window resizing, occurs on them.

        A slot is a Python callable that you can connect to a widget’s signal to perform 
        some actions in response to user events. If a signal and a slot are connected, 
        then the slot will be called automatically every time the signal is emitted.

        Slot is a Python callable. In other words, slot can be a function, a method, 
        a class, or an instance of a class that implements .__call__()."""

        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        # In the case of exitAction, you connect its triggered() signal with the built-in
        # slot QMainWindow.close().
        # This way, if you select File → Exit, then your application will close.
        self.exitAction.triggered.connect(self.close)

        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        self.zoomInAction.triggered.connect(self.zoomIn)
        self.zoomOutAction.triggered.connect(self.zoomOut)

        # Connect Library actions
        self.showLibraryAction.triggered.connect(self.showLibrary)
        self.loadLibraryAction.triggered.connect(self.pickLibrary)
        self.refreshLibraryAction.triggered.connect(self.refreshLibrary)
        self.openExcelLibraryAction.triggered.connect(self.openExcelLibrary)

        # Connect Configuration actions
        self.globalConfigurationAction.triggered.connect(self.globalConfiguration)
        self.setenvConfigurationAction.triggered.connect(self.setenvConfiguration)

        # Connect Simulate actions
        self.startSimulateAction.triggered.connect(self.startSimulate)
        self.generateReportAction.triggered.connect(self.generateReport)

        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)

        # Connect About actions
        self.aboutAction.triggered.connect(self.about)

        # Connect Open Recent to dynamically populate it
        self.openRecentMenu.aboutToShow.connect(self.populateOpenRecent)

    # Slots

    def newFile(self):
        # Logic for creating a new file goes here...
        self.centralWidget.setText("<b>File > New mooring</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Open a mooring...</b> clicked")

    def saveFile(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Save mooring</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def zoomIn(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Zoom in mooring</b> clicked")

    def zoomOut(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Zoom out mooring</b> clicked")

    def showLibrary(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Library > Show </b> clicked")

    def pickLibrary(self):
        # Logic for pasting content goes here...
        # self.libraryDockWidget.hide()
        (self.libraryFileName, _) = QFileDialog.getOpenFileName(
            self, ("Open File"), "Library", ("Spreadsheet  (*.xls)"))
        self.loadLibrary()

    def loadLibrary(self):
        self.editToolBar.setDisabled(False)
        self.library = WidgetLibrary(self.libraryFileName)
        self.library.setMinimumWidth(floor(self.screen_width/2))
        self.library.setMinimumHeight(200)
        self.libraryDockWidget = QDockWidget()
        self.libraryDockWidget.setWidget(self.library)
        #Ajoute la bibliotheque dans le DockWidget en position haute#
        self.addDockWidget(Qt.TopDockWidgetArea,
                           self.libraryDockWidget)
        self.libraryDockWidget.setWindowTitle('Library')
        # send a signal to statusbar for testing only
        self.trigger.emit()

    def refreshLibrary(self):
        """ insert doc here"""
        if self.editToolBar.isEnabled():
            self.library.read()
            print("je passe")
            self.library.libraryLayout.removeWidget(self.library.libraryArea)
            self.library.libraryArea.close()
            self.library.display()
            self.library.libraryLayout.addWidget(self.library.libraryArea)
        else:
            self.loadLibrary()
            self.library.display()

    def openExcelLibrary(self):
        # Logic for pasting content goes here...
        #self.centralWidget.setText("<b> Library > openExcel </b> clicked")
        startfile(self.libraryFileName)

    def globalConfiguration(self):

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        # create the configuration panel
        self.config = QWidget()
        self.config.setWindowTitle('Global configuration')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        screen_width = QLineEdit(str(self.frameGeometry().width()))
        screen_height = QLineEdit(str(self.frameGeometry().height()))
        originCombo = QComboBox()
        originCombo.addItems(["bottom", "surface"])
        index = originCombo.findText(self.cfg['config']['origin'], Qt.MatchFixedString)
        if index >= 0:
             originCombo.setCurrentIndex(index)
        # connect signal to function selectOrigin, pass argument with functools.partial
        screen_width.textEdited.connect(partial(self.selectScreenWidth, screen_width))
        #screen_width.textEdited.connect(self.selectScreenWidth)
        originCombo.activated.connect(partial(self.selectOrigin, originCombo))
        bottom_depth = QLineEdit(str(self.cfg['config']['bottom_depth']))
        formLayout.addRow("Screen width", screen_width)
        formLayout.addRow("Screen height", screen_height)
        formLayout.addRow("Origin", originCombo)
        formLayout.addRow("Bottom depth", bottom_depth)
        #self.setText(0,"Contact Details")
        btnBox = QDialogButtonBox()
        btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        btnBox.accepted.connect(self.acceptConfig)
        btnBox.rejected.connect(self.cancelConfig)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(btnBox)
        self.config.setLayout(dlgLayout)
 
        self.stackedLayout.addWidget(self.config)
        #self.setCentralWidget(self.config)

    def selectScreenWidth(self, width):
        print(f"New width: {width.text()}")
        self.cfg['global']['screen_width'] = width.text()

    def selectOrigin(self, comboBox):
        print(f"Origin Selected: {comboBox.currentText()}")
        self.cfg['config']['origin'] = comboBox.currentText()

    def acceptConfig(self):
        print(f"{self.cfg['global']['screen_width']} x {self.cfg['global']['screen_height']}")

    def cancelConfig(self):
        print("Configuration cancelled...")


    def setenvConfiguration(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText(
            "<b>setenv Configuration</b> clicked")

    def startSimulate(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText(
            "<b>Simulate > Start simulation</b> clicked")

    def generateReport(self, action=None):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Simulate > Generate report</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Simulate > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")

    def populateOpenRecent(self):
        # Step 1. Remove the old options from the menu
        self.openRecentMenu.clear()
        # Step 2. Dynamically create the actions
        actions = []
        filenames = [f"File-{n}" for n in range(5)]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentFile, filename))
            actions.append(action)
        # Step 3. Add the actions to the menu
        self.openRecentMenu.addActions(actions)

    def openRecentFile(self, filename):
        # Logic for opening a recent file goes here...
        self.centralWidget.setText(f"<b>{filename}</b> opened")

    def getWordCount(self):
        # Logic for computing the word count goes here...
        return len(self.centralWidget.text())

    def handle_trigger(self):
        self.wcLabel.setText(f"{self.getWordCount()} Words")

def processArgs():
    parser = argparse.ArgumentParser(
        description='Mooring simulator program ',
        usage='\npython MooringSimulator.py --file <file> --lib <file> -d -h\n'
        ' \n',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='J. Grelet IRD US191 - March 2021 / April 2021')
    parser.add_argument('--file',
                        help='Mooring design file')
    parser.add_argument('--lib',
                        help='Libray definition file, Excel or JSON')
    parser.add_argument('-s', '--size',
                        nargs='+', type=int, default=[],
                        help='select screen size, default is 800 x 600')
    parser.add_argument('-r', '--reset', help='reset toml configuration file to default',
                        action='store_true')
    parser.add_argument('-d', '--debug', help='display debug informations',
                        action='store_true')
    return parser

def getDefaultConfig():
    toml_string = """

    [global]
    author  = "jgrelet IRD March 2021"
    debug   = false
    echo    = true
    screen_width = 800
    screen_height = 600

    [tools]
    name = 'tools/Angulate.xls'

    [config]
    origin = 'surface'  # or bottom
    bottom_depth = 0
    library = 'library/example.xls'
    """
    return toml.loads(toml_string)

def saveDefaultConfig():
        with open(theConfig, 'w') as fid:
            cfg = getDefaultConfig()
            cfg['version'] = VERSION
            toml.dump(cfg, fid)


if __name__ == "__main__":
    ''' Mooring simulator program entry point''' 

    # setup toml configuration file
    theConfig = Path(path.expandvars('$APPDATA/' + __file__)).with_suffix('.toml')
    if not path.isfile(theConfig):
        print (f"Configuration file don't exist, create one from default config to {theConfig}")
        saveDefaultConfig()

    # if no match in the version numbers, we reload the default configuration
    cfg = toml.load(theConfig)
    if not "version" in cfg or cfg["version"] != VERSION:
        saveDefaultConfig()
        cfg = toml.load(theConfig)

    # debug
    print(f"Version: {cfg['version']}, debug: {cfg['global']['debug']}")

    # Recover and process optionnal line arguments
    parser = processArgs()
    args = parser.parse_args()
    # load command line given library 
    if args.lib is None:
        library = path.normpath(cfg['config']['library'])
    else:
        library = args.lib

    # reset config file
    if args.reset:
        saveDefaultConfig()
        cfg = toml.load(theConfig)


    # Create the application
    app = QApplication([])

    # Create and show splash screen
    # pixmap = QPixmap(":splash.png")
    # splash = QSplashScreen(pixmap)
    # splash.show()
    app.processEvents()

    # print(QStyleFactory.keys())
    app.setStyle("Fusion")

    # Setting the Application Icon on Windows
    app.setWindowIcon(QIcon(":windows-main.ico"))

    # Set application window size, 800 x 600 by default
    if len(args.size) == 1:
        screen_resolution = app.desktop().screenGeometry()
        cfg['global']['screen_width'], cfg['global']['screen_height'] = \
            screen_resolution.width(), screen_resolution.height()
    elif len(args.size) == 2:
        cfg['global']['screen_width'], cfg['global']['screen_height'] = \
            args.size[0], args.size[1]
    else:
        pass

    # Create and show the main window
    mainWindow = MainWindow(cfg, library)
    mainWindow.show()
    # Close the splash screen
    #splash.finish(mainWindow)

    # Run the event loop
    ret = app.exec_()

    # Get the main windows size and update configuration for next use
    cfg['global']['screen_width'] = mainWindow.frameGeometry().width()
    cfg['global']['screen_height'] = mainWindow.frameGeometry().height()

    # Debug config
    debug = cfg['global']['debug'] 
    cfg['global']['debug'] = not debug
    print(f"Geometry: {cfg['global']['screen_width']} x {cfg['global']['screen_height']}")

    # Save current config
    with open(theConfig, 'w') as f:
        toml.dump(cfg, f)
    # Exit
    sys.exit(ret)
