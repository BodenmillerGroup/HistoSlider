from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction

from histoslider.ui.tiles_view import TilesView


class TilesViewWidget(QWidget):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)

        self.tiles_view = TilesView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.tiles_view)

    def fit_all_tiles(self):
        self.tiles_view.fit_all_tiles()

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)

        fit_all_tiles_action = QAction(QIcon(":/icons/grid.png"), "Fit All Tiles", self)
        fit_all_tiles_action.triggered.connect(self.fit_all_tiles)
        toolbar.addAction(fit_all_tiles_action)

        return toolbar
