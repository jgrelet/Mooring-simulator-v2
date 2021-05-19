import unittest
import sys
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QApplication
"""All tests use the same single global instance of QApplication."""

from PyQt5.QtWidgets import QWidget
"""The tests individually instantiate the top-level window as a QWidget."""

from PyQt5.QtTest import QTest

from configWindow import ConfigWindow

'''
Run all test_* in dir test:
> python -m unittest  discover tests -v
> python -m unittest  discover -s tests -p 'test_*.py' -v
or
> make test
or configure testing with VSC. 
To enable testing, use the Python: Configure Tests command on the Command Palette.
See: https://code.visualstudio.com/docs/python/testing
'''

# Create an application global accessible from all tests.
app= QApplication( sys.argv )

class testConfigWindow(unittest.TestCase):

    def setUp( self ):
        """Initialize"""
        self.cfg = ConfigWindow("ConfigWindow", "1.0")
        self.cfg.displayGlobalConfig()

        self.glob = {
            'author': "jgrelet IRD March 2021",
            'debug': False,
            'echo': True,
            'screen_width': 800,
            'screen_height': 600
        }

        self.tools = { 
            'name': 'tools/Angulate.xls'
        }

        self.config = {
            'reference': 'surface',  # or bottom
            'bottom_depth': 0,
            'library': 'library/example.xls'
        }

    def test_glob(self):
        ''' test block ['global']'''
        d = self.cfg['global']
        for k in d.keys():
            self.assertEqual(d[k], self.glob[k])

    def test_tools(self):
        ''' test block ['tools']'''
        d = self.cfg['tools']
        for k in d.keys():
            self.assertEqual(d[k], self.tools[k])

    def test_config(self):
        ''' test block ['config']'''
        d = self.cfg['config']
        for k in d.keys():
            self.assertEqual(d[k], self.config[k])

    # def test_false(self):
    #     ''' test block ['false']'''
    #     d = self.cfg['false']
    #     self.assertEqual(d, None)

    def test_default_gui(self):
        ''' test default GUI '''
        self.assertEqual(int(self.cfg.screen_width.text()), self.glob['screen_width'])
        self.assertEqual(int(self.cfg.screen_height.text()), self.glob['screen_height'])
        self.assertEqual(self.cfg.reference.currentText(), self.config['reference'])
        self.assertEqual(int(self.cfg.bottom_depth.text()), self.config['bottom_depth'])

    def test_input_gui(self):
        ''' test input GUI '''
        # Clear and then type "1024" into the lineEdit widget
        self.cfg.screen_width.clear()
        QTest.keyClicks(self.cfg.screen_width, "1024")
        # Push OK with the left mouse button
        okWidget = self.cfg.btnBox.button(self.cfg.btnBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(self.cfg.screen_width.text(), "1024")




   


if __name__ == '__main__':
    unittest.main()
