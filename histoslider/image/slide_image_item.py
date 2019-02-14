import numpy as np
from PIL import Image
from PyQt5.QtCore import QRectF
from pyqtgraph import ImageItem

from histoslider.core.decorators import catch_error


class SlideImageItem(ImageItem):
    def __init__(self):
        ImageItem.__init__(self)
        self.setPxMode(False)
        self.setAutoDownsample(False)

    @catch_error('Cannot load the image')
    def load_image(self, filename: str, RGB=True):
        img = Image.open(filename)
        data = np.asarray(img, dtype=np.float32)
        self.setImage(data)
        self.prepareGeometryChange()

    @catch_error('Cannot attach the image')
    def attach_image(self, img, RGB=True):
        self.setImage(img)
        self.prepareGeometryChange()

    def boundingRect(self):
        if self.image is not None:
            size = self.image.shape
        else:
            size = (0, 0)
        return QRectF(0, 0, size[0], size[1])
