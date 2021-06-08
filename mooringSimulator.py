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
from PyQt5.QtGui import QIcon, QPixmap
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

def startLogging(appName, debug=False):
        # create logger
        # logger = logging.getLogger('simple_example')
        # logger.setLevel(logging.DEBUG)
        # # create formatter
        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')
        # # create console handler and set level to debug
        # fh = logging.StreamHandler()
        # fh.setLevel(logging.DEBUG)
        if debug:
            logging.basicConfig(
            format='%(levelname)s:%(module)s %(funcName)s %(message)s', level=logging.DEBUG)
        #     fh = logging.StreamHandler()
        # else:
        #     fh = logging.FileHandler(Path(appName).with_suffix('.log'))
        # # add formatter to fh
        # fh.setFormatter(formatter)
        # # add fh to logger
        # logger.addHandler(fh)
        
# main function
if __name__ == "__main__":
    ''' Mooring simulator program entry point'''

    # Create the application handler
    app = QApplication([])

    appName = Path(__file__).with_suffix('').stem
    
    # Recover and process optionnal line arguments
    parser = processArgs()
    args = parser.parse_args()

    # start logging
    startLogging(appName, args.debug)

    # Create and show the main application window
    mainAppWindow = MainAppWindow()

    # load command line given library
    if args.lib is None:
        mainAppWindow.library = path.normpath(
            mainAppWindow.cfg['config']['library'])
    else:
        mainAppWindow.library = args.lib

    # reset config file
    if args.reset:
        mainAppWindow.cfg.saveDefaultConfig()
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
        mainAppWindow.cfg['global']['screenWidth'], mainAppWindow.cfg['global']['screenHeight'] = \
            screen_resolution.width(), screen_resolution.height()
    elif len(args.size) == 2:
        mainAppWindow.cfg['global']['screenWidth'], mainAppWindow.cfg['global']['screenHeight'] = \
            args.size[0], args.size[1]
    else:
        pass

    mainAppWindow.show()
    # Close the splash screen
    # splash.finish(mainAppWindow)

    # Run the event loop
    ret = app.exec_()

    # GetmainWindow. the main windows size and update configuration for next use
    #mainAppWindow.cfg['global']['screenWidth'] = mainAppWindow.frameGeometry().width()
    #mainAppWindow.cfg['global']['screenHeight'] = mainAppWindow.frameGeometry().height()

    # Debug config
    debug = mainAppWindow.cfg['global']['debug']
    mainAppWindow.cfg['global']['debug'] = not debug

    # Save current config
    mainAppWindow.cfg.saveConfig()
    logging.debug(print(mainAppWindow.cfg))

    # Exit
    sys.exit(ret)
