from typing import List

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsView, QGraphicsScene
from qimage2ndarray import array2qimage

from histoslider.core.manager import Manager
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import scale_image
from histoslider.libs.QtImageViewer import QtImageViewer


class MergeView(QtImageViewer):
    def __init__(self, parent: QWidget):
        QtImageViewer.__init__(self, parent)

        self.items: List[ChannelImageItem] = None

    def clear(self):
        super().clear()
        self.items = None

    def set_images(self, items: List[ChannelImageItem], blend_mode=QPainter.CompositionMode_Plus):
        self.items = items
        if items is None or len(items) == 0:
            return
        images = []
        for item in items:
            image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
            images.append(array2qimage(image, normalize=False))

        self.drawImages(images, blend_mode)

    def drawImages(self, images: List[QImage], blend_mode):
        result = QImage(images[0].size(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(result)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(images[0].rect(), Qt.transparent)
        painter.setCompositionMode(blend_mode)
        for i in images:
            painter.drawImage(0, 0, i)
        painter.end()

        self.setImage(result)

    def refresh_images(self):
        self.set_images(self.items)

    def set_blend_mode(self, mode):
        blend_mode = getattr(QPainter, mode)
        self.set_images(self.items, blend_mode)
