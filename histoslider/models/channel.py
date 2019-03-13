from __future__ import annotations

from PyQt5.QtGui import QIcon
from numpy.core.multiarray import ndarray
import numpy as np
import cv2
from pyqtgraph import makeARGB

from histoslider.image.channel_settings import ChannelSettings
from histoslider.models.base_data import BaseData


class Channel(BaseData):
    def __init__(self, label: str, meta: dict, image: ndarray):
        super().__init__(label, meta)
        self._image = image
        self.settings = ChannelSettings(image)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-compact-camera-16.png")

    @property
    def tooltip(self):
        return "Acquisition channel"

    @property
    def label(self) -> str:
        return self.meta["Label"] if "Label" in self.meta else None

    @property
    def metal(self) -> str:
        return self.meta["Metal"] if "Metal" in self.meta else None

    @property
    def mass(self) -> float:
        return float(self.meta["Mass"]) if "Mass" in self.meta else None

    @property
    def image(self):
        return self._image.astype(dtype=np.float32)

    def get_scaled(self):
        # scale = self.settings.max
        # result = rescaleData(self._image, 255.0/(self.settings.levels[1] - self.settings.levels[0]), 0)
        # result = self._image * (scale/(self.settings.levels[1] - self.settings.levels[0]))
        scale = self.settings.max
        minL = self.settings.levels[0]
        maxL = self.settings.levels[1]
        result = self.image * (scale / (maxL - minL))
        # result = cv2.convertScaleAbs(self.image, alpha=(scale / (maxL - minL)))
        return result.astype(dtype=np.float32)

    def get_normalized(self):
        # result = cv2.normalize(self.image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_16U)
        result = self.image.astype(dtype=np.float32)
        return result

    def get_argb(self):
        argb, alpha = makeARGB(self.image, levels=self.settings.levels, useRGBA=True)
        return argb
