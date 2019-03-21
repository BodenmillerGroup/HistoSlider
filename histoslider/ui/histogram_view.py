from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.ui.histogram_item import HistogramItem


class HistogramView(HistogramItem):
    def __init__(self, image_item: ChannelImageItem, blend_view=None):
        HistogramItem.__init__(self, image_item, bounds=(image_item.channel.settings.min, image_item.channel.settings.max))
        labelStyle = {'font-size': '10pt'}
        self.axis.setLabel(image_item.channel.label, **labelStyle)
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
