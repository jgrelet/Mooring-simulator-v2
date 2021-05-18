import unittest
import sys
from PyQt5.QtWidgets import QApplication
"""All tests use the same single global instance of QApplication."""

from PyQt5.QtWidgets import QWidget
"""The tests individually instantiate the top-level window as a QWidget."""

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

    def create_application_window( self ):
        w = QWidget()
        return w

    def setUp( self ):
        self.window = self.create_application_window()

        """Initialisation des tests."""
        self.cfg = ConfigWindow("ConfigWindow", "1.0")

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
            'origin': 'surface',  # or bottom
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

    def test_false(self):
        ''' test block ['false']'''
        d = self.cfg['false']
        self.assertEqual(d, None)

   


if __name__ == '__main__':
    unittest.main()
