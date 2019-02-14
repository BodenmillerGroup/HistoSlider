from pyqtgraph import ViewBox, mkPen

from histoslider.image.slide_graphics_item import SlideGraphicsItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel_data import ChannelData
from histoslider.models.slide_data import SlideData


class TileImageView(ViewBox):
    def __init__(self, parent, item):
        pen = mkPen("d", width=1)
        ViewBox.__init__(self, parent, border=pen, lockAspect=True, name=item.name)
        loaded = False
        slide_graphics_item = SlideGraphicsItem()
        if isinstance(item, SlideData):
            slide_data: SlideData = item
            if slide_data.slide_type == SlideType.TIFF:
                slide_graphics_item.load_image(slide_data.path, True)
                loaded = True
        elif isinstance(item, ChannelData):
            channel_data: ChannelData = item
            slide_graphics_item.attach_image(channel_data.img, False)
            loaded = True

        if loaded:
            self.addItem(slide_graphics_item.image_item)
