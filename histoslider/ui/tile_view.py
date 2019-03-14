from pyqtgraph import ViewBox, mkPen

from histoslider.image.channel_image_item import ChannelImageItem


class TileView(ViewBox):
    def __init__(self, parent, image_item: ChannelImageItem):
        ViewBox.__init__(self, parent, border=mkPen("d", width=1), lockAspect=True, name=image_item.channel.metal, invertY=True)
        self.addItem(image_item, ignoreBounds=False)
