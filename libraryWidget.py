# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A class that allows to display a library of components in table panel."""

import logging
from PyQt6 import QtGui # QIcon
from PyQt6 import QtWidgets
"""(
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QMdiArea,
    QScrollArea,
    QGridLayout,
)"""

from excel2json import excel2json
from constants import STYLE_SPREADSHEET_TEXT
from version import NAME


class LibraryWidget(QtWidgets.QTabWidget):
    """This class display a library in a tab panel.
    """

    def __init__(self, filename):
        """LibraryWidget constructor

        Args:
            filename (string): The Excel .xls library file
        """
        super(QtWidgets.QTabWidget, self).__init__()

        self.__logger = logging.getLogger(NAME)

        self.fileName = filename
        self.libraryLayout = QtWidgets.QVBoxLayout(self)

        # convert Excel to JSON to python dict
        self.library = self.read()

        # Initialize tab screen
        #self.tabWidget = QtWidgets.QTabWidget()
        #self.libraryArea = self.display()
        self.libraryArea = self.display()
        self.libraryLayout.addWidget(self.libraryArea)
        self.setLayout(self.libraryLayout)
        self.resize(400, 201)
        #sheet_names = library.worksheets

    def read(self):
        """Read and convert Excel file to JSON Python dictionary

        Returns:
            dict: a dictionary description of the library file
        """
        return excel2json(self.fileName)

    def display(self):
        """Display library inside MDI window in table panel

        Returns:
            QtWidgets.QMdiArea: an instance of a QtWidgets.QMdiArea object
        """
        #libraryArea = QtWidgets.QMdiArea(self)
        library = self.library.toDict()
        for worksheet in self.library.worksheets:
            libraryWidget = QtWidgets.QWidget()
            self.addTab(libraryWidget, worksheet)
            #cate = libraryArea.addSubWindow(libraryWidget)
            #cate.setWindowTitle(worksheet)
            #cate.setWindowIcon(QtGui.QIcon('exit24.png'))
            # display each subwindows with tab layout
            #libraryArea.setViewMode(QtWidgets.QMdiArea.ViewMode.SubWindowView)
            
            groupLayout = QtWidgets.QVBoxLayout()
            scrollArea = QtWidgets.QScrollArea()
            groupLayout.addWidget(scrollArea)
            scrolledWidget = QtWidgets.QWidget()
            # display the first layout grid with desciption (names) of each column
            grid = QtWidgets.QGridLayout(scrolledWidget)
            names = list(library[worksheet]['1'].keys())
            for col, name in enumerate(names):
                label = QtWidgets.QLabel(name)
                label.setStyleSheet(STYLE_SPREADSHEET_TEXT)
                grid.addWidget(label, 0, col)
            # for each row
            rows = list(library[worksheet].keys())
            for ind_row, row in enumerate(rows):
                # display column value
                columns = list(library[worksheet][row].keys())
                for col, name in enumerate(columns):
                    self.__logger.debug(
                        f"col: {col}, {type(col)},name: {name}, {type(name)}")
                    label = QtWidgets.QLabel(str(library[worksheet][row][name]))
                    color = 'black' if col else 'red'
                    if not ind_row:
                        color = 'green'
                    styleSheet = f"background-color : white; color : {color}; border: 1px solid black"
                    label.setStyleSheet(styleSheet)
                    grid.addWidget(label, 1+ind_row, col)
            grid.setSpacing(0)
            scrollArea.setWidget(scrolledWidget)
           
            libraryWidget.setLayout(groupLayout)

        #return libraryArea
        return libraryWidget
