"""ConfigWindow class, part of Mooring simulator PySide6 application."""

from os import path, makedirs
from pathlib import Path
import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox
from PySide6.QtWidgets import QDialogButtonBox, QApplication
from PySide6.QtCore import QSize, Qt
import toml
from appdirs import AppDirs
from version import NAME, AUTHOR
from logger import configure_logger


class ConfigWindow(QWidget):
    ''' This class display configuration window, and save in toml file
        TODOs: reset main windows with new dimensions 
    '''

    def __init__(self, app_name, version):
        #super(QWidget, self).__init__()
        super(ConfigWindow, self).__init__()

        # private properties
        self.__logger = logging.getLogger(NAME)
        self.__version = version

        # setup toml configuration file, see:
        # https://github.com/ActiveState/appdirs/blob/master/appdirs.py
        self.__config_dir = AppDirs(app_name, AUTHOR).user_config_dir
        if not path.exists(self.__config_dir):
            makedirs(self.__config_dir)
        self.__config_file = Path(path.expandvars(
            f"{self.__config_dir}/{app_name}")).with_suffix('.toml')
        if not path.isfile(self.__config_file):
            self.save_default_config()
        self.__cfg = toml.load(self.__config_file)
        if "version" not in self.__cfg or self.__cfg["version"] != self.__version:
            self.save_default_config()
            self.__cfg = toml.load(self.__config_file)

        # Lock the window to a fixed size. In Qt sizes are defined using a QSize object.
        # This accepts width and height parameters in that order
        self.setFixedSize(QSize(250, 200))
        self.reference = QComboBox()
        self.screen_width = QLineEdit(str(self.__cfg['global']['screen_width']))
        self.screen_height = QLineEdit(
            str(self.__cfg['global']['screen_height']))
        self.bottom_depth = QLineEdit(str(self.__cfg['config']['bottom_depth']))
        self.btn_box = QDialogButtonBox()

        # Create the stacked layout
        # self.stackedLayout = QStackedLayout()

    # overloading operators
    def __getitem__(self, key):
        ''' overload r[key] '''
        if key not in self.__cfg:
            self.__logger.warning("invalid key: \"%s\"", key)
            return None
        return self.__cfg[key]

    def __str__(self):
        config_str = f"\n\
        User config dir = {self.__config_file}\n\
        Window size = {self.__cfg['global']['screen_width']} x {self.__cfg['global']['screen_height']}\n\
        Reference = {self.__cfg['config']['reference']} \n\
        Bottom depth = {self.__cfg['config']['bottom_depth']} \n\
        Debug = {self.__cfg['global']['debug']}"
        return config_str

    def display_global_config(self):
        """ Build and display the configuration panel
        """
        self.setWindowTitle('Global configuration')
        dialog_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.screen_width.setInputMask("0000")
        self.screen_height.setInputMask("0000")
        self.reference.addItems(["surface", "bottom"])
        index = self.reference.findText(
            self.__cfg['config']['reference'], Qt.MatchFixedString)
        if index >= 0:
            self.reference.setCurrentIndex(index)
        self.bottom_depth.setInputMask("0000")
        form_layout.addRow("Screen width", self.screen_width)
        form_layout.addRow("Screen height", self.screen_height)
        form_layout.addRow("Origin", self.reference)
        form_layout.addRow("Bottom depth", self.bottom_depth)
        self.btn_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.cancel)
        # Set the layout on the dialog
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(self.btn_box)
        self.setLayout(dialog_layout)

        # self.stackedLayout.addWidget(self.config)
        # self.setCentralWidget(self.config)

    def accept(self):
        """accept fuction when button OK is pressed"""
        self.__cfg['global']['screen_width'] = int(self.screen_width.text())
        self.__cfg['global']['screen_height'] = int(self.screen_height.text())
        self.__cfg['config']['reference'] = str(self.reference.currentText())
        self.__cfg['config']['bottom_depth'] = int(self.bottom_depth.text())
        self.save_config()
        self.close()
        # prevent QWidget::setLayout: Attempting to set QLayout which already has a layout
        # in display_global_config::self.setLayout(dialog_layout)
        # TODOS: verify below
        # QObjectCleanupHandler().add(self.layout())

    def cancel(self):
        """Configuration cancelled"""
        self.__logger.info("Configuration cancelled...")
        self.close()

    def save_config(self):
        """Save current config"""
        with open(self.__config_file, 'w', encoding="utf-8") as fid:
            toml.dump(self.__cfg, fid)

    def save_default_config(self):
        """Save default configuration to file"""
        self.__logger.info(
            "Configuration file don't exist, create one from default config to %s", 
            self.__config_file)
        with open(self.__config_file, 'w', encoding="utf-8") as fid:
            self.__cfg = ConfigWindow.get_default_config()
            self.__cfg['version'] = self.__version
            toml.dump(self.__cfg, fid)

    @staticmethod
    def get_default_config():
        """define default toml configuration file"""
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

    logger = configure_logger('DEBUG')

    # Create the application
    app = QApplication([])

    # remove path and file extention, get only the filename
    appn = Path(__file__).with_suffix('').stem

    cfg = ConfigWindow(appn, "1.03")
    cfg.display_global_config()
    cfg.show()

    # Run the event loop
    app.exec_()
    print(cfg)
