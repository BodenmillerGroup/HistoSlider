from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SelectedChannelChangedMessage, SlideRemovedMessage, SlideUnloadedMessage
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.models.channel import Channel


class OriginView(ImageView, HubListener):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "OriginView")
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        histogram_lut_item = self.getHistogramWidget().item
        histogram_lut_item.sigLevelsChanged.connect(self._on_levels_changed)
        histogram_lut_item.sigLookupTableChanged.connect(self._on_lookup_table_changed)
        self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

        self.channel: Channel = None

    def register_to_hub(self, hub):
        hub.subscribe(self, SelectedChannelChangedMessage, self._on_selected_channel_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_levels_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        if self.channel.settings.levels is None:
            self.autoLevels()
        self.channel.settings.levels = self.getHistogramWidget().item.getLevels()

    def _on_lookup_table_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        lut = self.getHistogramWidget().item.getLookupTable(n=round(self.channel.settings.levels[1]), alpha=0.5)
        self.channel.settings.lut = lut

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_selected_channel_changed(self, message: SelectedChannelChangedMessage):
        if not isinstance(message.channel, Channel):
            return

        slide_graphics_item = ChannelImageItem()
        self.channel = message.channel
        slide_graphics_item.setImage(self.channel.image)
        self.setImage(slide_graphics_item.image, levels=self.channel.settings.levels)
        self.getImageItem().setLookupTable(self.channel.settings.lut)
        self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    def clear(self):
        self.channel = None
        super().clear()
