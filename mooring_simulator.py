# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Mooring simulator, an Python/Qt application for designing oceanographic moorings."""

import sys
from os import path
from pathlib import Path
import argparse
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from logger import configure_logger
from main_app_window import MainAppWindow


def process_args():
    """Process optional command line argument

    Returns:
        argparse: an instance of argparse class
    """
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
    parser.add_argument('-l', '--log', help='save log informations',
                        action='store_true')
    return parser

# Mooring simulator main program entry point
if __name__ == "__main__":

    # Create the application handler
    app = QApplication([])

    appName = Path(__file__).with_suffix('').stem

    # Recover and process optionnal line arguments
    p = process_args()
    args = p.parse_args()

    # start logging
    #logger = configure_logger(stream_level='DEBUG' if args.debug else 'INFO', 
    # debug_file=Path(appName).with_suffix('.log'))
    #global logger
    logger = configure_logger(stream_level='DEBUG' if args.debug else 'INFO',
                              debug_file=Path(appName).with_suffix('.log') if args.log else None)
    logger.info("The program starts")

    # Create and show the main application window
    #main_app_window = Main_app_window('test_logging')
    main_app_window = MainAppWindow()

    # load command line given library
    if args.lib is None:
        main_app_window.library = path.normpath(
            main_app_window.cfg['config']['library'])
    else:
        main_app_window.library = args.lib

    # reset config file
    if args.reset:
        main_app_window.cfg.save_default_config()
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
        main_app_window.cfg['global']['screen_width'], 
        main_app_window.cfg['global']['screen_height'] = \
            screen_resolution.width(), screen_resolution.height()
    elif len(args.size) == 2:
        main_app_window.cfg['global']['screen_width'], 
        main_app_window.cfg['global']['screen_height'] = \
            args.size[0], args.size[1]
    else:
        pass

    main_app_window.show()
    # Close the splash screen
    # splash.finish(main_app_window)

    # Run the event loop
    ret = app.exec_()

    # GetmainWindow. the main windows size and update configuration for next use
    #main_app_window.cfg['global']['screen_width'] = main_app_window.frameGeometry().width()
    #main_app_window.cfg['global']['screen_height'] = main_app_window.frameGeometry().height()

    # Debug config, just for testing, change debug value each time of the program is started
    debug = main_app_window.cfg['global']['debug']
    main_app_window.cfg['global']['debug'] = not debug

    # Save current config
    main_app_window.cfg.save_config()
    logger.debug(main_app_window.cfg)

    # Exit
    logger.info("End of the program ...")
    sys.exit(ret)
