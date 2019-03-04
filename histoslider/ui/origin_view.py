from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, ShowItemChangedMessage, \
    SlideUnloadedMessage
from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide


class OriginView(ImageView, HubListener):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "OriginView")
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_current_item_changed(self, message: TreeViewCurrentItemChangedMessage):
        loaded = False
        slide_graphics_item = SlideImageItem()
        if isinstance(message.item, Slide):
            slide_data: Slide = message.item
            if slide_data.slide_type == SlideType.TIFF:
                slide_graphics_item.load_image(slide_data.slide_path, True)
                loaded = True
        elif isinstance(message.item, Channel):
            channel_data: Channel = message.item
            slide_graphics_item.attach_image(channel_data.image, False)
            loaded = True

        if loaded:
            self.setImage(slide_graphics_item.image)
            self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
