from typing import List

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.image.channel_image_item import ChannelImageItem


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
            hue_rotations = np.linspace(0, 1, len(items))
            blend_image = None
            alpha = 0.5
            for i, item in enumerate(items):
                ch = item.channel
                argb = ch.get_argb()
                # argb = cv2.cvtColor(argb, cv2.COLOR_GRAY2RGB)
                # argb = colorize(argb, hue_rotations[i], saturation=1)
                if blend_image is None:
                    blend_image = argb
                else:
                    # blend_image = alpha * blend_image + (1 - alpha) * tinted_image
                    # blend_image = cv2.add(blend_image, argb)
                    # blend_image = blend_image + argb
                    blend_image = cv2.add(blend_image, argb)
            self.setImage(blend_image)

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()
