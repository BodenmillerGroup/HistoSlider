from typing import Union

import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from openslide import open_slide, OpenSlide, ImageSlide


class OpenSlideImage:
    # This class is a wrapper for the OpenSlide class in order to integrate it into a QT application
    def __init__(self):
        self.filename: str = None
        self.img: Union[OpenSlide, ImageSlide] = None
        self.RGB = True

    def load_slide(self, filename: str, RGB=True):
        self.filename = filename
        self.RGB = RGB
        self.img = open_slide(filename)

    def attach_image(self, img, RGB=True):
        # Loads a (slide) image
        self.RGB = RGB
        # self.img will be an OpenSlide class image
        self.img = ImageSlide(Image.fromarray(img))

    def getPixmap(self, level: int, x: int, y: int, width: int, height: int) -> QPixmap:
        """
        :param level: zoom level
        :param x: x coordinates
        :param y: y coordinates
        :param width: window width
        :param height: window height
        :return: qt
        """
        img = self.img.read_region((x, y), level, (width, height))
        img_qt = ImageQt(img)
        pixmap = QPixmap.fromImage(img_qt)
        return pixmap

    def getNumpyImage(self, level: int, x: int, y: int, width: int, height: int):
        """
        :param level: zoom level
        :param x: x coordinates
        :param y: y coordinates
        :param width: window width
        :param height: window height
        :return: qt
        """
        img = self.img.read_region((x, y), level, (width, height))
        # convert the image to an array
        if self.RGB:
            img_array = np.asarray(img)
        else:
            img_array = np.asarray(img)[:, :, 0]
        img_array = img_array.swapaxes(0, 1)
        return img_array

    @property
    def dimensions(self):
        if self.img is None:
            return (0, 0)
        else:
            return self.img.dimensions

    @property
    def level_dimensions(self):
        if self.img is None:
            return (0, 0)
        else:
            return self.img.level_dimensions

    def get_best_level_for_downsample(self, downsample: float):
        if self.img is not None:
            return self.img.get_best_level_for_downsample(downsample)
        else:
            return 0

    @property
    def level_downsamples(self):
        if self.img is not None:
            return self.img.level_downsamples
        else:
            return [1]

    def close(self):
        if self.img is not None:
            self.img.close()
