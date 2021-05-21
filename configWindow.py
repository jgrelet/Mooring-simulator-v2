"""ConfigWindow class, part of Mooring simulator PyQt5 application."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObjectCleanupHandler #, QObject, pyqtSignal
from functools import partial
from os import path, makedirs
from pathlib import Path
import toml
import logging


class ConfigWindow(QWidget):
    ''' This class display configuration window, and save in toml file
    '''
    def __init__(self, pathName, appName, version):
        super(QWidget, self).__init__()

        self.version = version
         # setup toml configuration file, may be move in init function.
        self.configPath = path.expandvars(f"$APPDATA/{pathName}")
        if not path.exists(self.configPath):
            makedirs(self.configPath)
        self.configFile = Path(path.expandvars(f"{self.configPath}/{appName}")).with_suffix('.toml')
        if not path.isfile(self.configFile):
            self.saveDefaultConfig()
        self.__cfg = toml.load(self.configFile)
        if not "version" in self.__cfg or self.__cfg["version"] != self.version:
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
            logging.error(" file_extractor.py: invalid key: \"{}\"".format(key))
            return None
        else:
            return self.__cfg[key]

    def __str__(self):
        logging.debug(f"Window size = {self.__cfg['global']['screenWidth']} x {self.__cfg['global']['screenHeight']}")
        logging.debug(f"Reference = {self.__cfg['config']['reference']}")
        logging.debug(f"Bottom depth = {self.__cfg['config']['bottomDepth']}")
        return 'Je passe'
        
    def displayGlobalConfig(self):
        """ Build and display the configuration panel
        """
        self.setWindowTitle('Global configuration')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.screenWidth = QLineEdit(str(self.__cfg['global']['screenWidth']))
        self.screenWidth.setInputMask("0000")
        self.screenHeight = QLineEdit(str(self.__cfg['global']['screenHeight']))
        self.screenHeight.setInputMask("0000")
        self.reference = QComboBox()
        self.reference.addItems([ "surface","bottom"])
        index = self.reference.findText(self.__cfg['config']['reference'], Qt.MatchFixedString)
        if index >= 0:
             self.reference.setCurrentIndex(index)
        self.bottomDepth = QLineEdit(str(self.__cfg['config']['bottomDepth']))
        self.bottomDepth.setInputMask("0000")
        formLayout.addRow("Screen width", self.screenWidth)
        formLayout.addRow("Screen height", self.screenHeight)
        formLayout.addRow("Origin", self.reference)
        formLayout.addRow("Bottom depth", self.bottomDepth)
        self.btnBox = QDialogButtonBox()
        self.btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.cancel)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(self.btnBox)
        self.setLayout(dlgLayout)
 
        #self.stackedLayout.addWidget(self.config)
        #self.setCentralWidget(self.config)

    def accept(self):
        self.__cfg['global']['screenWidth'] = int(self.screenWidth.text())
        self.__cfg['global']['screenHeight'] = int(self.screenHeight.text())
        self.__cfg['config']['reference'] = str(self.reference.currentText())
        self.__cfg['config']['bottomDepth'] = int(self.bottomDepth.text())
        self.saveConfig()
        self.close()
        # prevent QWidget::setLayout: Attempting to set QLayout which already has a layout
        # in displayGlobalConfig::self.setLayout(dlgLayout)
        QObjectCleanupHandler().add(self.layout())

    def cancel(self):
        logging.debug("Configuration cancelled...")
        self.close()
    
    # Save current config
    def saveConfig(self): 
        with open(self.configFile, 'w') as fid:
            toml.dump(self.__cfg, fid)

    def saveDefaultConfig(self):
        logging.info(f"Configuration file don't exist, create one from default config to {self.configFile}")
        with open(self.configFile, 'w') as fid:
            self.__cfg = ConfigWindow.getDefaultConfig()
            self.__cfg['version'] = self.version
            toml.dump(self.__cfg, fid)

    @staticmethod
    def getDefaultConfig():
        toml_string = """
        [global]
        author  = "jgrelet IRD March 2021"
        debug   = false
        echo    = true
        screenWidth = 800
        screenHeight = 600

        [tools]
        name = 'tools/Angulate.xls'

        [config]
        reference = 'surface'  # or bottom
        bottomDepth = 0
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

    cfg = ConfigWindow(appName, "1.03")
    cfg.displayGlobalConfig() 
    cfg.show()

    # Run the event loop
    app.exec_()
    logging.debug(cfg)

