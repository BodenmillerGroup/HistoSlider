from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import ChannelImagesChangedMessage, SlideRemovedMessage, SlideUnloadedMessage
from histoslider.ui.tiles_view import TilesView


class TilesViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)

        self.tiles_view = TilesView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.tiles_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, ChannelImagesChangedMessage, self._on_channel_images_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.tiles_view.clear()

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def _on_channel_images_changed(self, message: ChannelImagesChangedMessage):
        self.tiles_view.set_images(message.images)

    def fit_all_tiles(self):
        self.tiles_view.fit_all_tiles()

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        fit_all_tiles_action = QAction(QIcon(":/icons/grid.png"), "Fit All Tiles", self)
        fit_all_tiles_action.triggered.connect(self.fit_all_tiles)
        toolbar.addAction(fit_all_tiles_action)

        return toolbar
