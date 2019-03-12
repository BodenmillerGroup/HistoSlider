from typing import Tuple

from numpy.core.multiarray import ndarray


class ChannelSettings:
    def __init__(self, image: ndarray):
        self.min, self.max = image.min(), image.max()
        self.levels: Tuple[float, float] = (self.min, self.max)
        self.lut: ndarray = None
        self.color_multiplier: Tuple[int, int, int] = (1, 1, 1)

    def set_levels(self, levels: Tuple[float, float]):
        self.levels = levels

    def set_lut(self, lut: ndarray):
        self.lut = lut

    def set_color_multiplier(self, multiplier: Tuple[int, int, int]):
        self.color_multiplier = multiplier
