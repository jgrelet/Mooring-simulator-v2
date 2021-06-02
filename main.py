import sys
from PyQt5.QtWidgets import QApplication
from mooringSimulator import MooringSimulator
from PyQt5.QtGui import QIcon


def main():
    app = QApplication(sys.argv)

    args = app.arguments()


    app.processEvents()
    # print(QStyleFactory.keys())
    app.setStyle("Fusion")

    # Setting the Application Icon on Windows
    app.setWindowIcon(QIcon(":windows-main.ico"))

    ex = MooringSimulator(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
