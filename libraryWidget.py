# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mooring simulator PyQt application."""

#import sys
#from functools import partial

#from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon  # , QKeySequence
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QMdiArea,
    QScrollArea,
    QGridLayout,
)
from excel2json import excel2json
import logging


class LibraryWidget(QWidget):
    ''' this class display library'''

    def __init__(self, filename):
        super(QWidget, self).__init__()
        self.fileName = filename
        self.libraryLayout = QVBoxLayout(self)

        # convert Excel to JSON to python dict
        self.library = self.read()

        # Initialize tab screen
        self.tabWidget = QTabWidget()
        self.libraryArea = self.display()
        self.libraryLayout.addWidget(self.libraryArea)
        self.setLayout(self.libraryLayout)
        self.resize(400, 201)
        #sheet_names = library.worksheets

    def read(self):
        ''' read and convert Excel file to JSON python dict'''
        return excel2json(self.fileName)

    
    def display(self):
        ''' display library inside MDI window '''
        libraryArea = QMdiArea(self)
        library = self.library.toDict()
        for worksheet in self.library.worksheets:
            libraryWidget = QWidget()
            cate = libraryArea.addSubWindow(libraryWidget)
            cate.setWindowTitle(worksheet)
            cate.setWindowIcon(QIcon('exit24.png'))
            # display each subwindows with tab layout
            libraryArea.setViewMode(1)
            groupLayout = QVBoxLayout()
            scrollArea = QScrollArea()
            groupLayout.addWidget(scrollArea)
            scrolledWidget = QWidget()
            # display the first layout grid with desciption (names) of each column
            grid = QGridLayout(scrolledWidget)
            names = list(library[worksheet]['1'].keys())
            for col, name in enumerate(names):
                label = QLabel(name)
                label.setStyleSheet(
                    "QLabel { font: bold; background-color : white; color : black;border: 2px solid black }")
                grid.addWidget(label, 0, col)
            # for each row
            rows = list(library[worksheet].keys())
            for ind_row, row in enumerate(rows):
                # display column value
                columns = list(library[worksheet][row].keys())
                for col, name in enumerate(columns):
                    #logging.debug(f"col: {col}, {type(col)},name: {name}, {type(name)}")
                    label = QLabel(str(library[worksheet][row][name]))
                    color = 'black' if col else 'red' 
                    if not ind_row: color = 'green' 
                    styleSheet = f"background-color : white; color : {color}; border: 1px solid black"
                    label.setStyleSheet(styleSheet)
                    grid.addWidget(label, 1+ind_row, col)
            grid.setSpacing(0)
            scrollArea.setWidget(scrolledWidget)
            libraryWidget.setLayout(groupLayout)

        return libraryArea
