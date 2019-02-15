from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView

from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage
from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel_data import ChannelData
from histoslider.core.data_manager import DataManager
from histoslider.models.slide_data import SlideData


class BlendView(ImageView, HubListener):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "SlideImageView")
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        self.getHistogramWidget().hide()

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_current_item_changed(self, message: TreeViewCurrentItemChangedMessage):
        loaded = False
        slide_graphics_item = SlideImageItem()
        if isinstance(message.item, SlideData):
            slide_data: SlideData = message.item
            if slide_data.slide_type == SlideType.TIFF:
                slide_graphics_item.load_image(slide_data.path, True)
                loaded = True
        elif isinstance(message.item, ChannelData):
            channel_data: ChannelData = message.item
            slide_graphics_item.attach_image(channel_data.image, False)
            loaded = True

        if loaded:
            self.setImage(slide_graphics_item.image)
            self.getHistogramWidget().show()
