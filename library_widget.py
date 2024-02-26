# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A class that allows to display a library of components in table panel."""

import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMdiArea,
    QScrollArea,
    QGridLayout,
)

from excel2json import excel2json
from constants import STYLE_SPREADSHEET_TEXT
from version import NAME


class LibraryWidget(QWidget):
    """This class display a library in a table panel.
    """

    def __init__(self, filename):
        """LibraryWidget constructor

        Args:
            filename (string): The Excel .xls library file
        """
        #super(QWidget, self).__init__()
        super(LibraryWidget, self).__init__()

        self.__logger = logging.getLogger(NAME)

        self.file_name = filename
        self.library_layout = QVBoxLayout(self)

        # convert Excel to JSON to python dict
        self.library = self.read()

        # Initialize tab screen
        #self.tabWidget = QTabWidget()
        self.library_area = self.display()
        self.library_layout.addWidget(self.library_area)
        self.setLayout(self.library_layout)
        self.resize(400, 201)
        #sheet_names = library.worksheets

    def read(self):
        """Read and convert Excel file to JSON Python dictionary

        Returns:
            dict: a dictionary description of the library file
        """
        return excel2json(self.file_name)

    def display(self):
        """Display library inside MDI window in table panel

        Returns:
            QMdiArea: an instance of a QMdiArea object
        """
        library_area = QMdiArea(self)
        library = self.library.toDict()
        for worksheet in self.library.worksheets:
            library_widget = QWidget()
            cate = library_area.addSubWindow(library_widget)
            cate.setWindowTitle(worksheet)
            cate.setWindowIcon(QIcon('exit24.png'))
            # display each subwindows with tab layout
            library_area.setViewMode(1)
            group_layout = QVBoxLayout()
            scroll_area = QScrollArea()
            group_layout.addWidget(scroll_area)
            scrolled_widget = QWidget()
            # display the first layout grid with desciption (names) of each column
            grid = QGridLayout(scrolled_widget)
            names = list(library[worksheet]['1'].keys())
            for col, name in enumerate(names):
                label = QLabel(name)
                label.setStyleSheet(STYLE_SPREADSHEET_TEXT)
                grid.addWidget(label, 0, col)
            # for each row
            rows = list(library[worksheet].keys())
            for ind_row, row in enumerate(rows):
                # display column value
                columns = list(library[worksheet][row].keys())
                for col, name in enumerate(columns):
                    self.__logger.debug(
                        "col: %d, %s, name: %s, %s", col, type(col), name, type(name))
                    label = QLabel(str(library[worksheet][row][name]))
                    color = 'black' if col else 'red'
                    if not ind_row:
                        color = 'green'
                    style_sheet = \
                        f"background-color : white; color : {color}; border: 1px solid black"
                    label.setStyleSheet(style_sheet)
                    grid.addWidget(label, 1+ind_row, col)
            grid.setSpacing(0)
            scroll_area.setWidget(scrolled_widget)
            library_widget.setLayout(group_layout)

        return library_area
