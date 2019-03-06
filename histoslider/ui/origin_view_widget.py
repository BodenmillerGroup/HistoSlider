from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QComboBox, QLabel

from histoslider.ui.origin_view import OriginView


class OriginViewWidget(QWidget):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)

        self.origin_view = OriginView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.origin_view)

    def show_scale_bar(self, state: bool):
        self.origin_view.show_scale_bar(state)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self.show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        label = QLabel("View Mode:")
        toolbar.addWidget(label)

        combobox = QComboBox(toolbar)
        combobox.addItems(["Greyscale", "RGB", "CMY", "Heat"])
        toolbar.addWidget(combobox)

        return toolbar
