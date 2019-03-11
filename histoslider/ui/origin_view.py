from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.models.channel import Channel


class OriginView(ImageView):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "OriginView")
        histogram_lut_item = self.getHistogramWidget().item
        histogram_lut_item.sigLevelsChanged.connect(self._on_levels_changed)
        histogram_lut_item.sigLookupTableChanged.connect(self._on_lookup_table_changed)
        self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-40, -40))
        self.scale.hide()

        self.channel: Channel = None
        self.lut = None

    # FIX: https://stackoverflow.com/questions/50722238/pyqtgraph-imageview-and-color-images
    def updateImage(self, autoHistogramRange=True):
        super().updateImage(autoHistogramRange)
        self.getImageItem().setLookupTable(self.lut)

    def setLookupTable(self, lut):
        self.lut = lut
        self.updateImage()

    def _on_levels_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        if self.channel.settings.levels is None:
            self.autoLevels()
        self.channel.settings.levels = self.getHistogramWidget().item.getLevels()

    def _on_lookup_table_changed(self):
        if self.channel is None or self.getImageItem() is None:
            return
        lut = self.getHistogramWidget().item.getLookupTable(n=int(self.channel.settings.levels[1]), alpha=0.5)
        self.channel.settings.lut = lut

    def set_channel(self, channel: Channel):
        self.channel = channel
        self.setImage(self.channel.image, levels=self.channel.settings.levels)
        self.getImageItem().setLookupTable(self.channel.settings.lut)
        self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    def clear(self):
        self.getHistogramWidget().hide()
        self.channel = None
        super().clear()
