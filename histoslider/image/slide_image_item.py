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
        if len(data.shape) > 2:
            data = data.transpose([1, 0, 2])
        else:
            data = data.T
        self.setImage(data)

    def attach_image(self, img, RGB=True):
        # data = np.asarray(img, dtype=np.float32).T
        self.setImage(img)
