from typing import List

import cv2
import numpy as np
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
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

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

    def clear(self):
        super().clear()
        self.items = None

    def set_images(self, items: List[ChannelImageItem]):
        self.items = items
        if len(items) == 0:
            return
        blend_image = 0
        levels = []
        if len(items) == 1:
            blend_image = items[0].image
            levels = items[0].channel.settings.levels
        else:
            for item in items:
                image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
                blend_image = cv2.add(blend_image, image)
                levels.append(item.channel.settings.levels)
                # if blend_image is None:
                #     blend_image = image
                # else:
                #     # blend_image = alpha * blend_image + (1 - alpha) * image
                #     # blend_image = np.add(blend_image, image)
                #     blend_image = cv2.add(blend_image, image)
                #     # blend_image = cv2.addWeighted(blend_image, alpha, image, 1 - alpha, 0)
                #     # blend_image = blend_method(blend_image, image, alpha)
        # try:
        #     self.getHistogramWidget().item.sigLevelChangeFinished.disconnect()
        # except TypeError:
        #     pass

        # self.getHistogramWidget().item.setLevelMode("rgba") if Manager.data.view_mode is ViewMode.RGB else self.getHistogramWidget().item.setLevelMode("mono")
        self.setImage(blend_image, autoHistogramRange=False)
        # self.getHistogramWidget().item.autoHistogramRange()
        # self.setLevels([])
        # self.getHistogramWidget().show()
        if len(items) == 1:
            self.setLevels(*items[0].channel.settings.levels)
            # self.getHistogramWidget().item.sigLevelChangeFinished.connect(self._on_level_change_finished)
        else:
            # mx = np.amax(blend_image)
            self.setLevels(*max(levels))
            # self.getHistogramWidget().item.autoHistogramRange()
            # self.setLevels(*levels)
            pass

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
