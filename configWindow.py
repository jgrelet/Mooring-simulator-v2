"""ConfigWindow class, part of Mooring simulator PyQt5 application."""

from PyQt5.QtWidgets import * # QWidget, QVBoxLayout
from PyQt5.QtCore import QSize, Qt, QObjectCleanupHandler
from os import path, makedirs
from pathlib import Path
import toml
import logging
from appdirs import AppDirs
from version import NAME, AUTHOR
from logger import configure_logger


class ConfigWindow(QWidget):
    ''' This class display configuration window, and save in toml file
        TODOs: reset main windows with new dimensions 
    '''

    def __init__(self, appName, version):
        super(QWidget, self).__init__()

        # private properties
        self.__logger = logging.getLogger(NAME)
        self.__version = version

        # setup toml configuration file, see:
        # https://github.com/ActiveState/appdirs/blob/master/appdirs.py
        self.__config_dir = AppDirs(appName, AUTHOR).user_config_dir
        if not path.exists(self.__config_dir):
            makedirs(self.__config_dir)
        self.__config_file = Path(path.expandvars(
            f"{self.__config_dir}/{appName}")).with_suffix('.toml')
        if not path.isfile(self.__config_file):
            self.saveDefaultConfig()
        self.__cfg = toml.load(self.__config_file)
        if not "version" in self.__cfg or self.__cfg["version"] != self.__version:
            self.saveDefaultConfig()
            self.__cfg = toml.load(self.__config_file)

        # Lock the window to a fixed size. In Qt sizes are defined using a QSize object.
        # This accepts width and height parameters in that order
        self.setFixedSize(QSize(250, 200))

        # Create the stacked layout
        # self.stackedLayout = QStackedLayout()

    # overloading operators
    def __getitem__(self, key):
        ''' overload r[key] '''
        if key not in self.__cfg:
            self.__logger.warning("invalid key: \"{}\"".format(key))
            return None
        else:
            return self.__cfg[key]

    def __str__(self):
        str = f"\n\
        User config dir = {self.__config_file}\n\
        Window size = {self.__cfg['global']['screenWidth']} x {self.__cfg['global']['screenHeight']}\n\
        Reference = {self.__cfg['config']['reference']} \n\
        Bottom depth = {self.__cfg['config']['bottomDepth']} \n\
        Debug = {self.__cfg['global']['debug']}"
        return str

    def displayGlobalConfig(self):
        """ Build and display the configuration panel
        """
        self.setWindowTitle('Global configuration')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.screenWidth = QLineEdit(str(self.__cfg['global']['screenWidth']))
        self.screenWidth.setInputMask("0000")
        self.screenHeight = QLineEdit(
            str(self.__cfg['global']['screenHeight']))
        self.screenHeight.setInputMask("0000")
        self.reference = QComboBox()
        self.reference.addItems(["surface", "bottom"])
        index = self.reference.findText(
            self.__cfg['config']['reference'], Qt.MatchFixedString)
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

        # self.stackedLayout.addWidget(self.config)
        # self.setCentralWidget(self.config)

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
        self.__logger.info("Configuration cancelled...")
        self.close()

    # Save current config
    def saveConfig(self):
        with open(self.__config_file, 'w') as fid:
            toml.dump(self.__cfg, fid)

    def saveDefaultConfig(self):
        self.__logger.info(
            f"Configuration file don't exist, create one from default config to {self.__config_file}")
        with open(self.__config_file, 'w') as fid:
            self.__cfg = ConfigWindow.getDefaultConfig()
            self.__cfg['version'] = self.__version
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

    logger = configure_logger('DEBUG')

    # Create the application
    app = QApplication([])

    # remove path and file extention, get only the filename
    appName = Path(__file__).with_suffix('').stem

    cfg = ConfigWindow(appName, "1.03")
    cfg.displayGlobalConfig()
    cfg.show()

    # Run the event loop
    app.exec_()
    print(cfg)
