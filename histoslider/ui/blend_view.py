from typing import Dict

from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar, makeARGB
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

        self.channels: Dict[str, Channel] = dict()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

    def register_to_hub(self, hub):
        hub.subscribe(self, SlideRemovedMessage, self._on_slide_removed)
        hub.subscribe(self, SlideUnloadedMessage, self._on_slide_unloaded)
        hub.subscribe(self, CheckedChannelChangedMessage, self._on_checked_channel_changed)

    def _on_slide_removed(self, message: SlideRemovedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_slide_unloaded(self, message: SlideUnloadedMessage):
        self.getHistogramWidget().hide()
        self.clear()

    def _on_checked_channel_changed(self, message: CheckedChannelChangedMessage):
        channel = message.channel
        if isinstance(channel, Channel):
            if channel.checked:
                if channel.name not in self.channels:
                    self.channels[channel.name] = channel
            else:
                if channel.name in self.channels:
                    self.channels.pop(channel.name)

            if len(self.channels) > 0:
                blend_image = None
                alpha = 0.5
                for i, ch in enumerate(self.channels.values()):
                    argb, alpha = makeARGB(ch.image, lut=ch.settings.lut, levels=ch.settings.levels)
                    # argb = color.gray2rgb(ch.image, False)
                    if blend_image is None:
                        blend_image = argb
                    else:
                        blend_image = alpha * blend_image + (1 - alpha) * argb
                self.setImage(blend_image)
                self.getHistogramWidget().show()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
