from typing import List

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import colorize


class BlendView(ImageView):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "BlendView")
        # self.getHistogramWidget().hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

        self.lut = None

    # FIX: https://stackoverflow.com/questions/50722238/pyqtgraph-imageview-and-color-images
    def updateImage(self, autoHistogramRange=True):
        super().updateImage(autoHistogramRange)
        self.getImageItem().setLookupTable(self.lut)

    def setLookupTable(self, lut):
        self.lut = lut
        self.updateImage()

    def set_channels(self, items: List[ChannelImageItem]):
        if len(items) > 0:
            hue_rotations = np.linspace(0, 270, len(items), dtype=np.uint8)
            color_multipliers = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1))
            blend_image = None
            alpha = 0.5
            for i, item in enumerate(items):
                ch = item.channel
                image = ch.image
                image = cv2.convertScaleAbs(image, alpha=(255 / (ch.settings.levels[1] - ch.settings.levels[0])))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                # argb = colorize(rgb_image, hue_rotations[i], saturation=1)
                argb = rgb_image * color_multipliers[i]
                if blend_image is None:
                    blend_image = argb
                else:
                    # blend_image = alpha * blend_image + (1 - alpha) * argb
                    # blend_image = blend_image + argb
                    blend_image = cv2.add(blend_image, argb)
            self.setImage(blend_image)
            self.autoLevels()

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
