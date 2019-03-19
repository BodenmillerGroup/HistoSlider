from typing import List

import cv2
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.manager import Manager
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import scale_image
from histoslider.models.mask import Mask


class MaskView(ImageView):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "MaskView")
        # self.getHistogramWidget().hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        self.mask: Mask = None

    def clear(self):
        super().clear()
        self.mask = None

    def set_mask(self, mask: Mask):
        self.mask = mask
        if mask.loaded:
            self.setImage(mask.image)

    def refresh_images(self):
        self.set_images(self.items)
