"""ConfigWindow class, part of Mooring simulator PyQt5 application."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObjectCleanupHandler #, QObject, pyqtSignal
from functools import partial
from os import startfile, path
from pathlib import Path
import toml


class ConfigWindow(QWidget):
    ''' This class display configuration window, and save in toml file
    '''
    def __init__(self, appName, version):
        super(QWidget, self).__init__()

        self.version = version
         # setup toml configuration file, may be move in init function.
        self.configFile = Path(path.expandvars('$APPDATA/' + appName)).with_suffix('.toml')
        if not path.isfile(self.configFile):
            self.saveDefaultConfig()
        self.__cfg = toml.load(self.configFile)
        if not "version" in self.__cfg or self.__cfg["version"] != version:
            self.saveDefaultConfig()
            self.__cfg = toml.load(self.configFile)

        # Lock the window to a fixed size. In Qt sizes are defined using a QSize object. 
        # This accepts width and height parameters in that order
        self.setFixedSize(QSize(250,200))

        # Create the stacked layout
        #self.stackedLayout = QStackedLayout()

       # overloading operators
    def __getitem__(self, key):
        ''' overload r[key] '''
        if key not in self.__cfg:
            #logging.error(
            print(" file_extractor.py: invalid key: \"{}\"".format(key))
            return None
        else:
            return self.__cfg[key]

    def __str__(self):
        print(f"Window size = {self.__cfg['global']['screen_width']} x {self.__cfg['global']['screen_height']}")
        print(f"Reference = {self.__cfg['config']['reference']}")
        return(f"Bottom depth = {self.__cfg['config']['bottom_depth']}")

        
    def displayGlobalConfig(self):
        """ Build and display the configuration panel
        """
        self.setWindowTitle('Global configuration')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.screen_width = QLineEdit(str(self.__cfg['global']['screen_width']))
        self.screen_height = QLineEdit(str(self.__cfg['global']['screen_height']))
        self.reference = QComboBox()
        self.reference.addItems([ "surface","bottom"])
        index = self.reference.findText(self.__cfg['config']['reference'], Qt.MatchFixedString)
        if index >= 0:
             self.reference.setCurrentIndex(index)
        self.bottom_depth = QLineEdit(str(self.__cfg['config']['bottom_depth']))
        formLayout.addRow("Screen width", self.screen_width)
        formLayout.addRow("Screen height", self.screen_height)
        formLayout.addRow("Origin", self.reference)
        formLayout.addRow("Bottom depth", self.bottom_depth)
        btnBox = QDialogButtonBox()
        btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        btnBox.accepted.connect(self.accept)
        btnBox.rejected.connect(self.cancel)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(btnBox)
        self.setLayout(dlgLayout)
 
        #self.stackedLayout.addWidget(self.config)
        #self.setCentralWidget(self.config)

    def accept(self):
        self.__cfg['global']['screen_width'] = int(self.screen_width.text())
        self.__cfg['global']['screen_height'] = int(self.screen_height.text())
        self.__cfg['config']['reference'] = str(self.reference.currentText())
        self.__cfg['config']['bottom_depth'] = int(self.bottom_depth.text())
        self.saveConfig()
        self.close()
        # prevent QWidget::setLayout: Attempting to set QLayout which already has a layout
        # in displayGlobalConfig::self.setLayout(dlgLayout)
        QObjectCleanupHandler().add(self.layout())

    def cancel(self):
        #print("Configuration cancelled...")
        self.close()
    
    # Save current config
    def saveConfig(self): 
        with open(self.configFile, 'w') as fid:
            toml.dump(self.__cfg, fid)

    def saveDefaultConfig(self):
        print(f"Configuration file don't exist, create one from default config to {self.configFile}")
        with open(self.configFile, 'w') as fid:
            cfg = ConfigWindow.getDefaultConfig()
            cfg['version'] = self.version
            toml.dump(cfg, fid)

    @staticmethod
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
        reference = 'surface'  # or bottom
        bottom_depth = 0
        library = 'library/example.xls'
        """
        return toml.loads(toml_string)

# for testing in standalone context
# ---------------------------------
if __name__ == "__main__":

    # Create the application
    app = QApplication([])

    # remove path and file extention, get only the filename
    appName = Path(__file__).with_suffix('').stem

    cfg = ConfigWindow(appName, "1.02")
    cfg.displayGlobalConfig() 
    cfg.show()

    # Run the event loop
    app.exec_()
    print(cfg)

