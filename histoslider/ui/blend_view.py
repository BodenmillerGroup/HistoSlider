from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar
import numpy as np

from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, ShowItemChangedMessage, \
    SlideUnloadedMessage
from histoslider.image.slide_image_item import SlideImageItem
from histoslider.image.slide_type import SlideType
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide
from histoslider.core.data_manager import DataManager


class BlendView(ImageView, HubListener):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "BlendView")
        HubListener.__init__(self)
        self.register_to_hub(DataManager.hub)
        self.getHistogramWidget().hide()

        self.layers: Dict[str, object] = dict()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)
        hub.subscribe(self, ShowItemChangedMessage, self._on_show_item_changed)

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

    def _on_show_item_changed(self, message: ShowItemChangedMessage):
        item = message.item
        if isinstance(item, Channel):
            if item.checked:
                if not item.name in self.layers:
                    layer = item.image
                    self.layers[item.name] = layer
            else:
                if item.name in self.layers:
                    layer = self.layers[item.name]
                    self.layers.pop(item.name)

            if len(self.layers.values()) == 3:
                # blend_image = np.dstack(self.layers.values())
                images = list(self.layers.values())
                blend_image = np.zeros((images[0].shape[0], images[0].shape[1], 3))
                blend_image[:, :, 0] = images[0]
                blend_image[:, :, 1] = images[1]
                blend_image[:, :, 2] = images[2]
                self.setImage(blend_image)
                self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
