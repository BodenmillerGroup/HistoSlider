from typing import Tuple

from numpy.core.multiarray import ndarray


class ChannelSettings:
    def __init__(self, image: ndarray):
        self.min, self.max = image.min(), image.max()
        self.levels: Tuple[float, float] = (self.min, self.max)

    def set_levels(self, levels: Tuple[float, float]):
        self.levels = levels
