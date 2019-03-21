from typing import List

import cv2
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from qimage2ndarray import array2qimage

from histoslider.core.manager import Manager
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import scale_image
from histoslider.libs.QtImageViewer import QtImageViewer


class MergeView(QtImageViewer):
    def __init__(self, parent: QWidget):
        QtImageViewer.__init__(self)

        self.items: List[ChannelImageItem] = None

    def clear(self):
        super().clear()
        self.items = None

    def set_images(self, items: List[ChannelImageItem], blend_mode=None):
        self.items = items
        if items is None or len(items) == 0:
            return
        blend_image = 0
        levels = []
        if len(items) == 1:
            blend_image = items[0].image
            levels.append(items[0].channel.settings.levels)
        else:
            for item in items:
                if blend_mode:
                    item.setCompositionMode(blend_mode)
                image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
                blend_image = cv2.addWeighted(blend_image, 0.5, image, 0.5, 0.0) if Manager.data.blend_mode == 'Weighted' else cv2.add(blend_image, image)
                levels.append(item.channel.settings.levels)

        qimage = array2qimage(blend_image, normalize=False)
        self.setImage(qimage)

    def refresh_images(self):
        self.set_images(self.items)

    def set_blend_mode(self, mode):
        blend_mode = getattr(QPainter, mode)
        self.set_images(self.items, blend_mode)
