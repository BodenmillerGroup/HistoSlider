from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from histoslider.core.decorators import catch_error
from histoslider.image.grey_image_item import GreyImageItem


class ImageItem(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None):
        QGraphicsItem.__init__(self, parent)
        self.image_item = GreyImageItem()

    @catch_error('Cannot load the image')
    def loadImage(self, filename: str, RGB=True):
        """
        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        self.image_item.load_image(filename, RGB)
        self.prepareGeometryChange()

    @catch_error('Cannot attach the image')
    def attachImage(self, img, RGB=True):
        """
        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        self.image_item.attach_image(img, RGB)
        self.prepareGeometryChange()

    def boundingRect(self):
        if self.image_item.image is not None:
            size = self.image_item.image.shape
        else:
            size = (0, 0)
        return QRectF(0, 0, size[0], size[1])

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        self.image_item.paint(painter)
