import numpy as np
from PIL import Image
from pyqtgraph import ImageItem


class SlideImageItem(ImageItem):
    def __init__(self):
        ImageItem.__init__(self)
        self.setPxMode(False)
        self.setAutoDownsample(False)

    def load_image(self, filename: str, RGB=True):
        img = Image.open(filename)
        data = np.asarray(img, dtype=np.float32)
        self.setImage(data)

    def attach_image(self, img, RGB=True):
        self.setImage(img)
