import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from lib.ui.CreateUICustom import CreateUICustom


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    """
    Starts Graphical User Interface App instead of command line
    """
    app = QtWidgets.QApplication(sys.argv)
    icon_file = resource_path('lib/ui/img/movie_icon.png')
    app.setWindowIcon(QIcon(icon_file))
    app.setQuitOnLastWindowClosed(False)

    ui = CreateUICustom(icon_file, app)
    ui.setupUi()
    ui.show()

    sys.exit(ui.exec_())


if __name__ == "__main__":
    main()
