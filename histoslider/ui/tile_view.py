from pyqtgraph import ViewBox, mkPen

from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.models.channel import Channel


class TileView(ViewBox):
    def __init__(self, parent, channel: Channel):
        ViewBox.__init__(self, parent, border=mkPen("d", width=1), lockAspect=True, name=channel.name, invertY=True)
        image_item = ChannelImageItem(channel.image, levels=channel.settings.levels, lut=channel.settings.lut)
        self.addItem(image_item, ignoreBounds=False)
