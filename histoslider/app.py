import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmapCache
from PyQt5.QtWidgets import QApplication
from pyqtgraph import setConfigOptions

from histoslider.core.manager import Manager
from histoslider.ui.main_window import MainWindow

# Global PyQtGraph settings
setConfigOptions(
    imageAxisOrder="row-major",
    foreground="d",
    background="w",
    leftButtonPan=True,
    antialias=False,
    useOpenGL=False,
    useWeave=False
)


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.setStyle('Fusion')
        self.setOrganizationName("UZH Zurich")
        self.setOrganizationDomain("http://www.bodenmillerlab.org")
        self.setApplicationName("HistoSlider")
        self.setWindowIcon(QIcon(":/icons/icons8-eukaryotic-cells-96.png"))

        cache_size_in_kb = 700 * 10 ** 3
        QPixmapCache.setCacheLimit(cache_size_in_kb)

        f = QFile(":/style.qss")
        f.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(QTextStream(f).readAll())
        f.close()

        # DataManager singleton initialization
        Manager()


def main():
    app = App(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
