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
    """ Test the configuration form GUI """

    def setUp( self ):
        """ Create and initialize to default the GUI"""
        self.form = ConfigWindow("ConfigWindow", "1.0")
        # restore the toml file to default config
        self.form.saveDefaultConfig()
        self.form.displayGlobalConfig()

        self.glob = {
            'author': "jgrelet IRD March 2021",
            'debug': False,
            'echo': True,
            'screenWidth': 800,
            'screenHeight': 600
        }

        self.tools = { 
            'name': 'tools/Angulate.xls'
        }

        self.config = {
            'reference': 'surface',  # or bottom
            'bottomDepth': 0,
            'library': 'library/example.xls'
        }

    def clearForm(self):
        """" Clear all line edit field """
        self.form.screenWidth.clear()
        self.form.screenHeight.clear()
        self.form.bottomDepth.clear()

    
    def test_0_defaults(self):
        ''' Test the GUI in its default state '''
        self.assertEqual(int(self.form.screenWidth.text()), self.glob['screenWidth'])
        self.assertEqual(int(self.form.screenHeight.text()), self.glob['screenHeight'])
        self.assertEqual(self.form.reference.currentText(), self.config['reference'])
        self.assertEqual(int(self.form.bottomDepth.text()), self.config['bottomDepth'])

    def test_1_glob(self):
        ''' test default config ['global']'''
        d = self.form['global']
        for k in d.keys():
            self.assertEqual(d[k], self.glob[k])

    def test_2_tools(self):
        ''' test default config ['tools']'''
        d = self.form['tools']
        for k in d.keys():
            self.assertEqual(d[k], self.tools[k])

    def test_3_config(self):
        ''' test default config ['config']'''
        d = self.form['config']
        for k in d.keys():
            self.assertEqual(d[k], self.config[k])

    # def test_false(self):
    #     ''' test block ['false']'''
    #     d = self.form['false']
    #     self.assertEqual(d, None)

 

    def test_screenWithLineEdit(self):
        ''' Test the screen width line edit '''
        # Clear and then type "1024" into the lineEdit widget
        #self.clearForm()
        QTest.keyClicks(self.form.screenWidth, "1024")
        # Push OK with the left mouse button
        okWidget = self.form.btnBox.button(self.form.btnBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(int(self.form.screenWidth.text()), 1024)


    def test_screenHeightLineEdit(self):
        ''' Test the screen height line edit '''
        # Clear and then type "768" into the lineEdit widget
        #self.clearForm()
        QTest.keyClicks(self.form.screenHeight, "768")
        # Push OK with the left mouse button
        okWidget = self.form.btnBox.button(self.form.btnBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(int(self.form.screenHeight.text()), 768)

    def test_referenceLineEdit(self):
        ''' Test the reference line edit '''
        # select into the reference comboBox widget
        #self.clearForm()
        QTest.keyClick(self.form.reference, Qt.Key_Down)
        self.assertEqual(self.form.reference.currentText(), "bottom")
        QTest.keyClick(self.form.reference, Qt.Key_Down)
        #self.assertEqual(self.form.reference.currentText(), "surface")
        # Push OK with the left mouse button
        okWidget = self.form.btnBox.button(self.form.btnBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)

    def test_bottomDepthLineEdit(self):
        ''' Test the bottom depth line edit '''
        # Clear and then type "4500" into the lineEdit widget
        #self.clearForm()
        QTest.keyClicks(self.form.bottomDepth, "4500")
        # Push OK with the left mouse button
        okWidget = self.form.btnBox.button(self.form.btnBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(int(self.form.bottomDepth.text()), 4500)



   


if __name__ == '__main__':
    unittest.main()
