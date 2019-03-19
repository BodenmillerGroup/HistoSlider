from PyQt5.QtWidgets import QVBoxLayout, QGroupBox

from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.libs.range_slider import QRangeSlider


class ChannelSettingsWidget(QGroupBox):
    def __init__(self, parent, image_item: ChannelImageItem, blend_view):
        QGroupBox.__init__(self, image_item.channel.label, parent)
        self.image_item = image_item
        self.blend_view = blend_view

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.range_slider = QRangeSlider(self)
        layout.addWidget(self.range_slider)

        self.range_slider.setMin(int(image_item.channel.settings.min))
        self.range_slider.setMax(int(image_item.channel.settings.max))
        mn, mx = image_item.channel.settings.levels
        self.range_slider.setRange(int(mn), int(mx))
        self.range_slider.startValueChanged.connect(self._on_levels_changed)
        self.range_slider.endValueChanged.connect(self._on_levels_changed)

    def _on_levels_changed(self):
        self.image_item.channel.settings.levels = self.range_slider.getRange()
        if self.blend_view is not None:
            self.blend_view.refresh_images()
