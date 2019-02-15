from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction

from histoslider.ui.blend_view import BlendView


class BlendViewWidget(QWidget):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)

        self.blend_view = BlendView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.blend_view)

    def show_scale_bar(self, state: bool):
        self.blend_view.show_scale_bar(state)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self.show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        return toolbar
