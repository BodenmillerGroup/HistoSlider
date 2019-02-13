import numpy as np
from PIL import Image
from pyqtgraph import ImageItem


class GreyImageItem(ImageItem):
    def __init__(self):
        ImageItem.__init__(self)
        self.setPxMode(False)
        self.setAutoDownsample(False)

    def load_image(self, filename: str, RGB=True):
        img = Image.open(filename)
        self.image = np.asarray(img, dtype=np.float32).T

    def attach_image(self, img, RGB=True):
        self.image = np.asarray(img, dtype=np.float32).T
