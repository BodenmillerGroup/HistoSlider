from pyqtgraph import ViewBox, mkPen

from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.slides.mcd.mcd_channel import McdChannel
from histoslider.slides.mcd.mcd_slide import McdSlide


class TileView(ViewBox):
    def __init__(self, parent, item):
        ViewBox.__init__(self, parent, border=mkPen("d", width=1), lockAspect=True, name=item.name, invertY=True)
        loaded = False
        slide_graphics_item = SlideImageItem()
        if isinstance(item, McdSlide):
            slide_data: McdSlide = item
            if slide_data.slide_type == SlideType.TIFF:
                slide_graphics_item.load_image(slide_data.file_path, True)
                loaded = True
        elif isinstance(item, McdChannel):
            channel_data: McdChannel = item
            slide_graphics_item.attach_image(channel_data.image, False)
            loaded = True

        if loaded:
            self.addItem(slide_graphics_item, ignoreBounds=False)
