from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from pyqtgraph import ImageItem

from histoslider.image.openslide_image import OpenSlideImage


class OpenSlideImageItem(ImageItem):
    """
    Expands the pyqtgraph ImageItem class to use a OpenSlideImage in the background
    """

    def __init__(self):
        ImageItem.__init__(self)
        self.setPxMode(False)
        self.setAutoDownsample(False)
        self.pos = (0, 0)
        self.scale = 1
        self.RGB = True
        self.slide_image = OpenSlideImage()

    def load_image(self, filename: str, RGB=True):
        self.slide_image.load_slide(filename, RGB)
        self.RGB = RGB

    def attach_image(self, img, RGB=True):
        self.slide_image.attach_image(img, RGB)
        self.RGB = RGB

    def update_image_region(self, level: int, x: int, y: int, width: int, height: int, autoLevels=False, **kargs):
        img = self.slide_image.getNumpyImage(level, x, y, width, height)
        self.setImage(img, autoLevels, **kargs)
        self.qimage = None

    def setPos(self, x: int, y: int):
        self.pos = (x, y)

    def setScale(self, scale):
        self.scale = scale

    def paint(self, p: QPainter, *args):
        if self.image is None:
            return
        if self.qimage is None:
            if self.RGB:
                self.lut = None
            self.render()
            if self.qimage is None:
                return
        if self.paintMode is not None:
            p.setCompositionMode(self.paintMode)

        p.drawImage(
            QRectF(self.pos[0], self.pos[1], self.image.shape[0] * self.scale, self.image.shape[1] * self.scale),
            self.qimage)
