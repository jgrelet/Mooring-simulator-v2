# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mooring simulator PyQt application."""

import sys
from os import path
from pathlib import Path
import argparse
import logging
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from mainAppWindow import MainAppWindow

def processArgs():
    parser = argparse.ArgumentParser(
        description='Mooring simulator program ',
        usage='\npython MooringSimulator.py --file <file> --lib <file> -d -h\n'
        ' \n',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='J. Grelet IRD US191 - March 2021 / April 2021')
    parser.add_argument('--file',
                        help='Mooring design file')
    parser.add_argument('--lib',
                        help='Libray definition file, Excel or JSON')
    parser.add_argument('-s', '--size',
                        nargs='+', type=int, default=[],
                        help='select screen size, default is 800 x 600')
    parser.add_argument('-r', '--reset', help='reset toml configuration file to default',
                        action='store_true')
    parser.add_argument('-d', '--debug', help='display debug informations',
                        action='store_true')
    return parser


# main function
if __name__ == "__main__":
    ''' Mooring simulator program entry point'''

    # Create the application
    app = QApplication([])

    # Create and show the main window
    mainWindow = MainAppWindow()

    # Recover and process optionnal line arguments
    parser = processArgs()
    args = parser.parse_args()
    # load command line given library
    if args.lib is None:
        mainWindow.library = path.normpath(mainWindow.cfg['config']['library'])
    else:
        mainWindow.library = args.lib

    # reset config file
    if args.reset:
        mainWindow.saveDefaultConfig()
        #cfg = toml.load(theConfig)

    # Create and show splash screen
    # pixmap = QPixmap(":splash.png")
    # splash = QSplashScreen(pixmap)
    # splash.show()
    app.processEvents()

    # print(QStyleFactory.keys())
    app.setStyle("Fusion")

    # Setting the Application Icon on Windows
    app.setWindowIcon(QIcon(":windows-main.ico"))

    # Set application window size, 800 x 600 by default
    if len(args.size) == 1:
        screen_resolution = app.desktop().screenGeometry()
        mainWindow.cfg['global']['screenWidth'], mainWindow.cfg['global']['screenHeight'] = \
            screen_resolution.width(), screen_resolution.height()
    elif len(args.size) == 2:
        mainWindow.cfg['global']['screenWidth'], mainWindow.cfg['global']['screenHeight'] = \
            args.size[0], args.size[1]
    else:
        pass

    mainWindow.show()
    # Close the splash screen
    # splash.finish(mainWindow)

    # Run the event loop
    ret = app.exec_()

    # GetmainWindow. the main windows size and update configuration for next use
    #mainWindow.cfg['global']['screenWidth'] = mainWindow.frameGeometry().width()
    #mainWindow.cfg['global']['screenHeight'] = mainWindow.frameGeometry().height()

    # Debug config
    debug = mainWindow.cfg['global']['debug']
    mainWindow.cfg['global']['debug'] = not debug

    # Save current config
    mainWindow.cfg.saveConfig()
    print(mainWindow.cfg)

    # Exit
    sys.exit(ret)
