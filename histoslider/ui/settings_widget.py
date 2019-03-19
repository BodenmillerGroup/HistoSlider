from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SlideRemovedMessage, SlideUnloadedMessage, \
    ChannelImagesChangedMessage
from histoslider.ui.channels_settings_widget import ChannelsSettingsWidget
from histoslider.ui.histograms_view import HistogramsView


class SettingsWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget, blend_view):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)
        self.blend_view = blend_view

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.tab_widget = QTabWidget(self)
        self.verticalLayout.addWidget(self.tab_widget)

        self.histograms_view = HistogramsView(self, blend_view)
        self.tab_widget.addTab(self.histograms_view, 'Histogram')

        self.channels_settings_widget = ChannelsSettingsWidget(self, blend_view)
        self.tab_widget.addTab(self.channels_settings_widget, 'Channels')

    def register_to_hub(self, hub):
        hub.subscribe(self, ChannelImagesChangedMessage, self._on_channel_images_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.histograms_view.clear()
        self.channels_settings_widget.clear()

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def _on_channel_images_changed(self, message: ChannelImagesChangedMessage):
        self.histograms_view.set_channels(message)
        self.channels_settings_widget.set_channels(message)
