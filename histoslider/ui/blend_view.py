from typing import List

import cv2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.manager import Manager
from histoslider.core.view_mode import ViewMode
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import colorize, scale_image
from histoslider.libs import blend_modes


class BlendView(ImageView):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "BlendView")
        self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

        # self.lut = None
        self.items: List[ChannelImageItem] = None

    # FIX: https://stackoverflow.com/questions/50722238/pyqtgraph-imageview-and-color-images
    # def updateImage(self, autoHistogramRange=True):
    #     super().updateImage(autoHistogramRange)
    #     self.getImageItem().setLookupTable(self.lut)

    # def setLookupTable(self, lut):
    #     self.lut = lut
    #     self.updateImage()

    def set_images(self, items: List[ChannelImageItem]):
        self.items = items
        if len(items) > 0:
            blend_image = None
            alpha = 0.5
            blend_method = getattr(blend_modes, Manager.data.blend_mode)
            for item in items:
                if len(items) == 1:
                    image = item.image
                else:
                    image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA) if Manager.data.view_mode is ViewMode.GREYSCALE else cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

                if blend_image is None:
                    blend_image = image
                else:
                    # blend_image = alpha * blend_image + (1 - alpha) * image
                    # blend_image = np.add(blend_image, image)
                    # blend_image = cv2.add(blend_image, image)
                    # blend_image = cv2.addWeighted(blend_image, alpha, image, 1 - alpha, 0)
                    blend_image = blend_method(blend_image, image, alpha)
            try:
                self.getHistogramWidget().item.sigLevelChangeFinished.disconnect()
            except TypeError:
                pass
            blend_image = cv2.cvtColor(blend_image, cv2.COLOR_RGBA2RGB)
            self.setImage(blend_image)
            if len(items) == 1:
                channel = items[0].channel
                self.setLevels(*channel.settings.levels)
                self.getHistogramWidget().item.sigLevelChangeFinished.connect(self._on_level_change_finished)
            self.getHistogramWidget().item.autoHistogramRange()
            self.getHistogramWidget().show()

    def refresh_images(self):
        self.set_images(self.items)

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    @pyqtSlot()
    def _on_level_change_finished(self):
        if self.items is None or len(self.items) != 1:
            return
        channel = self.items[0].channel
        levels = self.getHistogramWidget().item.getLevels()
        channel.settings.levels = levels

    def _on_lookup_table_changed(self):
        if self.items is None or len(self.items) != 1 or self.getImageItem() is None:
            return
        channel = self.items[0].channel
        lut = self.getHistogramWidget().item.getLookupTable(n=int(channel.settings.levels[1]), alpha=0.5)
        channel.settings.lut = lut
