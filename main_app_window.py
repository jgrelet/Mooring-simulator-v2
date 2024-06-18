# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mooring simulator PyQt application."""

import os
import sys
import subprocess
from functools import partial
from math import floor

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QIcon, QKeySequence, QAction
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMenu,
    QToolBar,
    QStyle,
    QFileDialog,
    QDockWidget,
)

from library_widget import LibraryWidget
from config_window import ConfigWindow
from version import NAME, APPNAME, VERSION

class MainAppWindow(QMainWindow, QObject):
    """Main window of the Mooring Simulator application
    The MainWindows class inherits from QMainWindow which is a prefabricated widget providing
    many standard window features that are used in the application, including toolbars, menus, 
    a status bar and more, menus, status bar, dockable widgets and more
    """

    # defined a signal named trigger as class attribute, used to display info on status bar
    # experimental...
    trigger = Signal()

    def __init__(self, library_file_name='', file_name=''):
        """In the class initializer .__init__(), you first call the parent class
        QMainWindow initializer using super(). Then you set the title of the window 
        using .setWindowTitle() and resize the window using .resize()
        """
        super(MainAppWindow, self).__init__()
        self.setWindowTitle(f"{NAME} v{VERSION}")

        # we use same name for directory and toml configuration file
        self.cfg = ConfigWindow(APPNAME, VERSION)
        self.resize(self.cfg['global']['screen_width'],
                    self.cfg['global']['screen_height'])
        self.file_name = file_name
        self.library_file_name = library_file_name

        # The window’s central widget is a QLabel object that you’ll use to show
        # messages in response to certain user actions. These messages will display
        # at the center of the window. To do this, you call .setAlignment() on the
        # QLabel object with a couple of alignment flags.
        self.central_widget = QLabel(
            f"Hello, welcome inside {NAME}, enjoy!")
        self.central_widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.central_widget)

        # Note that you call ._create_actions() before you call ._create_menu_bar() and
        # ._create_toolbars() because you’ll be using these actions on your menus and
        # toolbars.
        self._create_actions()
        self._create_menu_bar()
        self._create_toolbars()

        # Uncomment the call to ._createContextMenu() below to create a context
        # menu using menu policies. To test this out, you also need to
        # comment .context_menu_events() and uncomment ._createContextMenu()

        # self._createContextMenu()
        self._connect_actions()
        self._create_statusbar()

        # need to be modify because the path of the library is defined in the config file now
        # if library = args.lib not empty, load library directly
        if self.library_file_name:
            self.load_library()

    def _create_menu_bar(self):
        """In a PyQt main window–style application, QMainWindow provides an empty 
        QMenuBar object by default. To get access to this menu bar, you need to 
        call .menubar() on your QMainWindow object. This method will return an 
        empty menu bar. The parent for this menu bar will be your main window object."""

        # This is the preferred way of creating a menu bar in PyQt. Here, the menubar
        # variable will hold an empty menu bar, which will be your main window’s menu bar.
        menubar = self.menuBar()

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
        file_menu = QMenu("&File", self)
        menubar.addMenu(file_menu)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        # Creating menus using a title
        self.open_recent_menu = file_menu.addMenu("Open Recent")
        # You can add actions to a QMenu object using .addAction(). This method has
        # several variations. Most of them are thought to create actions on the fly.
        # We use a variation of .addAction() that QMenu inherits from QWidget:
        # QWidget.addAction(action)
        # The argument action represents the QAction object that you want to add to
        # a given QWidget object. With this variation of .addAction(), you can create
        # your actions beforehand and then add them to your menus as needed.
        file_menu.addAction(self.save_action)
        # Separator
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.cut_action)
        edit_menu.setDisabled(True)
        # Edit separator
        edit_menu.addSeparator()
        edit_menu.addAction(self.zoom_in_action)
        edit_menu.addAction(self.zoom_out_action)

        # Library menu
        library_menu = menubar.addMenu("&Library")
        library_menu.addAction(self.show_library_action)
        library_menu.addAction(self.load_library_action)
        library_menu.addAction(self.refresh_library_action)
        library_menu.addAction(self.open_excel_library_action)

        # Configuration menu
        configuration_menu = menubar.addMenu("&Configuration")
        configuration_menu.addAction(self.global_configuration_action)
        configuration_menu.addAction(self.setenv_configuration_action)

        # Simulate menu
        simulate_menu = menubar.addMenu("&Simulate")
        simulate_menu.addAction(self.start_simulate_action)
        simulate_menu.addAction(self.generate_report_action)
        simulate_menu.setDisabled(True)

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.help_content_action)
        help_menu.addAction(self.about_action)

    def _create_toolbars(self):
        # A toolbar is a movable panel that holds buttons and other widgets to provide
        # fast access to the most common options of a GUI application. Toolbar buttons
        # can display icons, text, or both to represent the task that they perform.
        # The base class for toolbars in PyQt is QToolBar. This class will allow you to
        # create custom toolbars for your GUI applications.

        # Create File toolbar using a title
        file_toolbar = self.addToolBar("File")
        file_toolbar.setMovable(False)
        file_toolbar.addAction(self.new_action)
        file_toolbar.addAction(self.open_action)
        file_toolbar.addAction(self.save_action)

        # Create Edit toolbar using a QToolBar object
        self.edit_toolbar = QToolBar("Edit", self)
        # inserts a QToolBar object (toolbar) into the specified toolbar area (area).
        # self.addToolBar(Qt.LeftToolBarArea, edit_toolbar)
        self.addToolBar(self.edit_toolbar)
        self.edit_toolbar.addAction(self.copy_action)
        self.edit_toolbar.addAction(self.paste_action)
        self.edit_toolbar.addAction(self.cut_action)
        self.edit_toolbar.addAction(self.zoom_in_action)
        self.edit_toolbar.addAction(self.zoom_out_action)
        self.edit_toolbar.setDisabled(True)

        # Library toolbar
        library_toolbar = QToolBar("Edit", self)
        self.addToolBar(library_toolbar)
        library_toolbar.addAction(self.show_library_action)
        library_toolbar.addAction(self.load_library_action)
        library_toolbar.addAction(self.refresh_library_action)
        library_toolbar.addAction(self.open_excel_library_action)

        # Adding Widgets to a Toolbar
        # First import the spin box class. Then create a QSpinBox object, set its
        # focusPolicy to Qt.NoFocus, and finally add it to the library toolbar.
        # self.fontSizeSpinBox = QSpinBox()
        # self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        # library_toolbar.addWidget(self.fontSizeSpinBox)

    def _create_statusbar(self):
        """ insert doc here"""
        self.statusbar = self.statusBar()
        # Temporary message
        self.statusbar.showMessage("Ready", 3000)
        # Permanent widget
        self.wc_label = QLabel(f"{self.get_word_count()} Words")
        self.statusbar.addPermanentWidget(self.wc_label)

    def _create_actions(self):
        """ insert doc here"""
        # File actions
        self.new_action = QAction(self)
        self.new_action.setText("&New mooring")
        self.new_action.setIcon(QIcon(self.style().standardIcon(getattr(QStyle,
                                                                       "SP_FileDialogNewFolder"))))
        self.open_action = QAction(
            QIcon(self.style().standardIcon(
                getattr(QStyle, "SP_DialogOpenButton"))),
            "&Open mooring", self)
        self.save_action = QAction(
            QIcon(self.style().standardIcon(
                getattr(QStyle, "SP_DialogSaveButton"))),
            "&Save mooring", self)
        self.exit_action = QAction("&Exit", self)
        # String-based key sequences
        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        # Help tips
        new_tip = "Design a new mooring"
        self.new_action.setStatusTip(new_tip)
        self.new_action.setToolTip(new_tip)
        self.new_action.setWhatsThis("Create a new and empty mooring")

        # Edit actions
        self.copy_action = QAction(QIcon(":edit-copy.png"), "&Copy", self)
        self.paste_action = QAction(QIcon(":edit-paste.png"), "&Paste", self)
        self.cut_action = QAction(QIcon(":edit-cut.png"), "C&ut", self)
        self.zoom_in_action = QAction(QIcon(":zoom-in.png"), "Zoom in", self)
        self.zoom_out_action = QAction(QIcon(":zoom-out.png"), "Zoom out", self)
        # Standard key sequence
        self.copy_action.setShortcut(QKeySequence.Copy)
        self.paste_action.setShortcut(QKeySequence.Paste)
        self.cut_action.setShortcut(QKeySequence.Cut)

        # Library actions
        self.show_library_action = QAction(
            QIcon(":library-show.png"), "&Show library", self)
        self.load_library_action = QAction(
            QIcon(":library-load-2.png"), "&Load new library", self)
        self.refresh_library_action = QAction(
            QIcon(":refresh.png"), "&Refresh library", self)
        self.open_excel_library_action = QAction(
            QIcon(":spreadsheet.png"), "&Open Excel library", self)
        # Standard key sequence
        # self.show_library_action.setShortcut(QKeySequence.Copy)
        # self.load_library_action.setShortcut(QKeySequence.Paste)

        # Configuration actions
        self.global_configuration_action = QAction(
            "Set global configuration", self)
        self.setenv_configuration_action = QAction(
            "Set environnemental conditions", self, checkable=True)

        # Simulate actions
        self.start_simulate_action = QAction(
            QIcon(":play.png"), "Start simulation", self)
        self.generate_report_action = QAction("Generate report", self)

        # Help actions
        self.help_content_action = QAction("&Help Content...", self)
        self.about_action = QAction("&About...", self)

        # Status bar actions
        # not well implemented
        # self.central_widgetAction = QAction(self.central_widget)
        # self.central_widget.addAction(self.central_widgetAction)
        self.trigger.connect(self.handle_trigger)

    # Uncomment this method to create a context menu using menu policies
    # def _createContextMenu(self):
    #     # Setting contextMenuPolicy
    #     self.central_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
    #     # Populating the widget with actions
    #     self.central_widget.addAction(self.new_action)
    #     self.central_widget.addAction(self.open_action)
    #     self.central_widget.addAction(self.save_action)
    #     self.central_widget.addAction(self.copy_action)
    #     self.central_widget.addAction(self.paste_action)
    #     self.central_widget.addAction(self.cut_action)

    def context_menu_events(self, event):
        """context menu event"""
        # Context menu
        menu = QMenu(self.central_widget)
        # Populating the menu with actions
        menu.addAction(self.new_action)
        menu.addAction(self.open_action)
        menu.addAction(self.save_action)
        # Separator
        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        menu.addAction(self.show_library)
        menu.addAction(self.pick_library)
        # Launching the menu
        menu.exec(event.globalPos())

    def _connect_actions(self):
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
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        # In the case of exit_action, you connect its triggered() signal with the built-in
        # slot QMainWindow.close().
        # This way, if you select File → Exit, then your application will close.
        self.exit_action.triggered.connect(self.close)

        # Connect Edit actions
        self.copy_action.triggered.connect(self.copy_content)
        self.paste_action.triggered.connect(self.paste_content)
        self.cut_action.triggered.connect(self.cut_content)
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action.triggered.connect(self.zoom_out)

        # Connect Library actions
        self.show_library_action.triggered.connect(self.show_library)
        self.load_library_action.triggered.connect(self.pick_library)
        self.refresh_library_action.triggered.connect(self.refresh_library)
        self.open_excel_library_action.triggered.connect(self.open_excel_library)

        # Connect Configuration actions
        self.global_configuration_action.triggered.connect(
            self.global_configuration)
        self.setenv_configuration_action.triggered.connect(
            self.setenv_configuration)

        # Connect Simulate actions
        self.start_simulate_action.triggered.connect(self.start_simulate)
        self.generate_report_action.triggered.connect(self.generate_report)

        # Connect Help actions
        self.help_content_action.triggered.connect(self.help_content)

        # Connect About actions
        self.about_action.triggered.connect(self.about)

        # Connect Open Recent to dynamically populate it
        self.open_recent_menu.aboutToShow.connect(self.populate_open_recent)

    # Slots

    def new_file(self):
        """ Logic for creating a new file goes here"""
        self.central_widget.setText("<b>File > New mooring</b> clicked")

    def open_file(self):
        """ Logic for opening an existing file goes here"""
        self.central_widget.setText("<b>File > Open a mooring...</b> clicked")

    def save_file(self):
        """ Logic for saving a file goes here"""
        self.central_widget.setText("<b>File > Save mooring</b> clicked")

    def copy_content(self):
        """ Logic for copying content goes here"""
        self.central_widget.setText("<b>Edit > Copy</b> clicked")

    def paste_content(self):
        """ Logic for pasting content goes here"""
        self.central_widget.setText("<b>Edit > Paste</b> clicked")

    def cut_content(self):
        """ Logic for cutting content goes here"""
        self.central_widget.setText("<b>Edit > Cut</b> clicked")

    def zoom_in(self):
        """ Logic for saving a file goes here"""
        self.central_widget.setText("<b>File > Zoom in mooring</b> clicked")

    def zoom_out(self):
        """ Logic for copying content goes here"""
        self.central_widget.setText("<b>Edit > Zoom out mooring</b> clicked")

    def show_library(self):
        """ Logic for pasting content goes here"""
        self.central_widget.setText("<b>Library > Show </b> clicked")

    def pick_library(self):
        """ Logic for pasting content goes here"""
        # self.library_dock_widget.hide()
        (self.library_file_name, _) = QFileDialog.getOpenFileName(
            self, ("Open File"), "Library", ("Spreadsheet  (*.xls)"))
        self.load_library()

    def load_library(self):
        """ Load library from file"""
        self.edit_toolbar.setDisabled(False)
        self.library = LibraryWidget(self.library_file_name)
        self.library.setMinimumWidth(
            floor(self.cfg['global']['screen_width']/2))
        self.library.setMinimumHeight(200)
        self.library_dock_widget = QDockWidget()
        self.library_dock_widget.setWidget(self.library)
        #Ajoute la bibliotheque dans le DockWidget en position haute#
        self.addDockWidget(Qt.TopDockWidgetArea,
                           self.library_dock_widget)
        self.library_dock_widget.setWindowTitle('Library')
        # send a signal to statusbar for testing only
        self.trigger.emit()

    def refresh_library(self):
        """ insert doc here"""
        if self.edit_toolbar.isEnabled():
            self.library.read()
            self.library.library_layout.removeWidget(self.library.library_area)
            self.library.library_area.close()
            self.library.display()
            self.library.library_layout.addWidget(self.library.library_area)
        else:
            self.load_library()
            self.library.display()

    def open_excel_library(self):
        """ insert doc here"""
        print(sys.platform)
        if sys.platform == "win32":
            os.startfile(self.library_file_name)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.library_file_name])

    def global_configuration(self):
        """ insert doc here"""
        self.cfg.display_global_config()
        self.cfg.show()

    def setenv_configuration(self):
        """ insert doc here"""
        # Logic for pasting content goes here...
        self.central_widget.setText(
            "<b>setenv Configuration</b> clicked")

    def start_simulate(self):
        """ insert doc here"""
        # Logic for pasting content goes here...
        self.central_widget.setText(
            "<b>Simulate > Start simulation</b> clicked")

    def generate_report(self, action=None):
        """ insert doc here"""
        # Logic for pasting content goes here...
        if action is not None:
            self.central_widget.setText("<b>Simulate > Generate report with action</b> clicked")
        else:
            self.central_widget.setText("<b>Simulate > Generate report without action</b> clicked")

    def help_content(self):
        """ insert doc here"""
        # Logic for launching help goes here...
        self.central_widget.setText("<b>Simulate > Help Content...</b> clicked")

    def about(self):
        """ insert doc here"""
        # Logic for showing an about dialog content goes here...
        self.central_widget.setText(f"<b>{NAME}:</b> {VERSION} - Build with PySide6")

    def populate_open_recent(self):
        """ insert doc here"""
        # Step 1. Remove the old options from the menu
        self.open_recent_menu.clear()
        # Step 2. Dynamically create the actions
        actions = []
        filenames = [f"File-{n}" for n in range(5)]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.open_recent_file, filename))
            actions.append(action)
        # Step 3. Add the actions to the menu
        self.open_recent_menu.addActions(actions)

    def open_recent_file(self, filename):
        """ insert doc here"""
        # Logic for opening a recent file goes here...
        self.central_widget.setText(f"<b>{filename}</b> opened")

    def get_word_count(self):
        """ insert doc here"""
        # Logic for computing the word count goes here...
        return len(self.central_widget.text())

    def handle_trigger(self):
        """ insert doc here"""
        self.wc_label.setText(f"{self.get_word_count()} Words")
