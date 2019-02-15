from pyqtgraph import ViewBox, mkPen

from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel_data import ChannelData
from histoslider.models.slide_data import SlideData


class TileView(ViewBox):
    def __init__(self, parent, item):
        ViewBox.__init__(self, parent, border=mkPen("d", width=1), lockAspect=True, name=item.name, invertY=True)
        loaded = False
        slide_graphics_item = SlideImageItem()
        if isinstance(item, SlideData):
            slide_data: SlideData = item
            if slide_data.slide_type == SlideType.TIFF:
                slide_graphics_item.load_image(slide_data.path, True)
                loaded = True
        elif isinstance(item, ChannelData):
            channel_data: ChannelData = item
            slide_graphics_item.attach_image(channel_data.image, False)
            loaded = True

        if loaded:
            self.addItem(slide_graphics_item, ignoreBounds=False)
