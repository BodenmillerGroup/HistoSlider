from __future__ import annotations

import numpy as np
from PyQt5.QtGui import QIcon
from numpy.core.multiarray import ndarray
from pyqtgraph import makeARGB

from histoslider.image.channel_settings import ChannelSettings
from histoslider.image.utils import scale_image
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
        if self._image is None:
            return np.zeros((1, 1))
        return self._image.astype(dtype=np.float32)

    def get_scaled(self):
        return scale_image(self.image, self.settings.max, self.settings.levels)

    def get_normalized(self):
        # result = cv2.normalize(self.image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_16U)
        result = self.image.astype(dtype=np.float32)
        return result

    def get_argb(self):
        argb, alpha = makeARGB(self.image, levels=self.settings.levels, useRGBA=True)
        return argb

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_image'] = None
        return state
