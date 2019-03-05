from pyqtgraph import ViewBox, mkPen

from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide


class TileView(ViewBox):
    def __init__(self, parent, item):
        ViewBox.__init__(self, parent, border=mkPen("d", width=1), lockAspect=True, name=item.name, invertY=True)
        loaded = False
        image_item = SlideImageItem()
        if isinstance(item, Slide):
            slide_data: Slide = item
            if slide_data.slide_type == SlideType.TIFF:
                image_item.load_image(slide_data.slide_path, True)
                loaded = True
        elif isinstance(item, Channel):
            channel: Channel = item
            image_item.setImage(channel.image, levels=channel.settings.levels, lut=channel.settings.lut)
            loaded = True

        if loaded:
            self.addItem(image_item, ignoreBounds=False)
