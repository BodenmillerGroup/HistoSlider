from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedChannelsChangedMessage
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.ui.blend_view import BlendView
from histoslider.ui.histograms_view import HistogramsView


class BlendViewWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)

        self.blend_view = BlendView(self)
        # self.histograms_view = HistogramsView(self)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.blend_view)
        # self.verticalLayout.addWidget(self.histograms_view)

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedChannelsChangedMessage, self._on_selected_channels_changed)

    def _on_selected_channels_changed(self, message: SelectedChannelsChangedMessage):
        items = []
        for channel in message.channels.values():
            items.append(ChannelImageItem(channel))
        self.blend_view.set_channels(items)
        # self.histograms_view.set_channels(items)

    def _show_scale_bar(self, state: bool):
        self.blend_view.show_scale_bar(state)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)

        show_scale_bar_action = QAction(QIcon(":/icons/icons8-ruler-16.png"), "Scale Bar", self)
        show_scale_bar_action.triggered.connect(self._show_scale_bar)
        show_scale_bar_action.setCheckable(True)
        toolbar.addAction(show_scale_bar_action)

        return toolbar
