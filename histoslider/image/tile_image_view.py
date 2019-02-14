from pyqtgraph import ViewBox

from histoslider.image.image_item import ImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel_data import ChannelData
from histoslider.models.slide_data import SlideData


class TileImageView(ViewBox):
    def __init__(self, parent, item):
        ViewBox.__init__(self, parent)
        loaded = False
        if isinstance(item, SlideData):
            slide_data: SlideData = item
            if slide_data.slide_type == SlideType.TIFF:
                graphItem = ImageItem()
                graphItem.loadImage(slide_data.path, True)
                loaded = True
        elif isinstance(item, ChannelData):
            channel_data: ChannelData = item
            graphItem = ImageItem()
            graphItem.attachImage(channel_data.img, False)
            loaded = True

        if loaded:
            # self.addItem(graphItem.image_item)
            pass
