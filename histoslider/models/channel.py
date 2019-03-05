from __future__ import annotations

from PyQt5.QtGui import QIcon
from numpy.core.multiarray import ndarray
from skimage import color

from histoslider.image.channel_settings import ChannelSettings
from histoslider.models.base_data import BaseData


class Channel(BaseData):
    def __init__(self, label: str, metal: str, mass: float, image: ndarray):
        super().__init__(label)
        self.metal = metal
        self.mass = mass
        self.image = image

        self.settings = ChannelSettings()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-compact-camera-16.png")

    @property
    def tooltip(self):
        return "Acquisition channel"

    @property
    def rgb_image(self):
        rgb = color.gray2rgb(self.image, False)
        return rgb * self.settings.color_multiplier
