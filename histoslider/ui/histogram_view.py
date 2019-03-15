from pyqtgraph import HistogramLUTItem

from histoslider.image.channel_image_item import ChannelImageItem


class HistogramView(HistogramLUTItem):
    def __init__(self, image_item: ChannelImageItem, blend_view=None):
        HistogramLUTItem.__init__(self, image_item, rgbHistogram=True)
        self.gradient.hide()
        self.blend_view = blend_view
        self.channel = image_item.channel
        self.setLevels(*self.channel.settings.levels)
        # self.sigLevelChangeFinished.connect(self._on_levels_changed)
        self.sigLevelsChanged.connect(self._on_levels_changed)

    def _on_levels_changed(self):
        if self.channel is None:
            return
        self.channel.settings.levels = self.getLevels()
        if self.blend_view is not None:
            self.blend_view.refresh_images()
