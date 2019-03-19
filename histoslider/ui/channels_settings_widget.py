from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from histoslider.core.message import ChannelImagesChangedMessage
from histoslider.ui.channel_settings_widget import ChannelSettingsWidget


class ChannelsSettingsWidget(QWidget):
    def __init__(self, parent=None, blend_view=None):
        QWidget.__init__(self, parent)
        self.blend_view = blend_view

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def clear(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def set_channels(self, message: ChannelImagesChangedMessage):
        self.clear()
        for item in message.images:
            item_widget = ChannelSettingsWidget(self, item, self.blend_view)
            self.layout().addWidget(item_widget)
