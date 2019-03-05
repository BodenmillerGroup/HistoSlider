from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar
from skimage import color

from histoslider.core.data_manager import DataManager
from histoslider.core.hub_listener import HubListener
from histoslider.core.message import SlideRemovedMessage, CheckedChannelChangedMessage, SlideUnloadedMessage
from histoslider.models.channel import Channel


class BlendView(ImageView, HubListener):

    color_multiplier = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1))

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
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)
        hub.subscribe(self, CheckedChannelChangedMessage, self._on_show_item_changed)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_show_item_changed(self, message: CheckedChannelChangedMessage):
        item = message.channel
        if isinstance(item, Channel):
            if item.checked:
                if item.name not in self.layers:
                    layer = item.image
                    self.layers[item.name] = layer
            else:
                if item.name in self.layers:
                    self.layers.pop(item.name)

            if len(self.layers) > 0:
                blend_image = None
                alpha = 0.5
                for i, layer in enumerate(self.layers.values()):
                    rgb_image = color.gray2rgb(layer, False)
                    if blend_image is None:
                        blend_image = rgb_image * self.color_multiplier[i]
                    else:
                        blend_image = alpha * blend_image + (1 - alpha) * (rgb_image * self.color_multiplier[i])
                self.setImage(blend_image)
                self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
