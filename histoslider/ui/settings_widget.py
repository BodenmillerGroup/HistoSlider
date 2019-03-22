from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from histoslider.core.hub_listener import HubListener
from histoslider.core.manager import Manager
from histoslider.core.message import SlideRemovedMessage, SlideUnloadedMessage, ChannelImagesChangedMessage
from histoslider.ui.channels_settings_widget import ChannelsSettingsWidget


class SettingsWidget(QWidget, HubListener):
    def __init__(self, parent: QWidget, blend_view):
        QWidget.__init__(self, parent)
        HubListener.__init__(self)
        self.register_to_hub(Manager.hub)
        self.blend_view = blend_view

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        self.channels_settings_widget = ChannelsSettingsWidget(self, blend_view)
        self.tab_widget.addTab(self.channels_settings_widget, 'Histograms')

    def register_to_hub(self, hub):
        hub.subscribe(self, ChannelImagesChangedMessage, self._on_channel_images_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def clear(self):
        self.channels_settings_widget.clear()

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.clear()

    def _on_channel_images_changed(self, message: ChannelImagesChangedMessage):
        self.channels_settings_widget.set_channels(message)
