"""ConfigWindow class, part of Mooring simulator PyQt5 application."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt #, QObject, pyqtSignal
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
         # setup toml configuration file
        self.configFile = Path(path.expandvars('$APPDATA/' + appName)).with_suffix('.toml')
        if not path.isfile(self.configFile):
            print(f"Configuration file don't exist, create one from default config to {self.configFile}")
            self.saveDefaultConfig()
        self.__cfg = toml.load(self.configFile)
        if not "version" in self.__cfg or self.__cfg["version"] != version:
            self.saveDefaultConfig()
            self.__cfg = toml.load(self.configFile)

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
        
    def displayGlobalConfig(self):
    
        # create the configuration panel
        #self.config = QWidget()
        #self.config.setWindowTitle('Global configuration')
        self.setWindowTitle('Global configuration')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        screen_width = QLineEdit(str(self.frameGeometry().width()))
        screen_height = QLineEdit(str(self.frameGeometry().height()))
        originCombo = QComboBox()
        originCombo.addItems(["bottom", "surface"])
        index = originCombo.findText(self.__cfg['config']['origin'], Qt.MatchFixedString)
        if index >= 0:
             originCombo.setCurrentIndex(index)
        # connect signal to function selectOrigin, pass argument with functools.partial
        screen_width.textEdited.connect(partial(self.selectScreenWidth, screen_width))
        #screen_width.textEdited.connect(self.selectScreenWidth)
        originCombo.activated.connect(partial(self.selectOrigin, originCombo))
        bottom_depth = QLineEdit(str(self.__cfg['config']['bottom_depth']))
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
        self.setLayout(dlgLayout)
 
        #self.stackedLayout.addWidget(self.config)
        #self.setCentralWidget(self.config)

    def selectScreenWidth(self, width):
        print(f"New width: {width.text()}")
        self.__cfg['global']['screen_width'] = width.text()

    def selectOrigin(self, comboBox):
        print(f"Origin Selected: {comboBox.currentText()}")
        self.__cfg['config']['origin'] = comboBox.currentText()

    def acceptConfig(self):
        print(f"{self.__cfg['global']['screen_width']} x {self.__cfg['global']['screen_height']}")

    def cancelConfig(self):
        print("Configuration cancelled...")
    
    def saveDefaultConfig(self):
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
        origin = 'surface'  # or bottom
        bottom_depth = 0
        library = 'library/example.xls'
        """
        return toml.loads(toml_string)

# for testing in standalone context
# ---------------------------------
if __name__ == "__main__":

    # Create the application
    app = QApplication([])

    appName = Path(__file__).with_suffix('').stem
    cfg = ConfigWindow(appName, "1.0")
    cfg.displayGlobalConfig() 

    cfg.show()

    # Run the event loop
    app.exec_()

