import numpy as np
from PIL import Image
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
