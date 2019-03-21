from __future__ import annotations

from typing import Type

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush

from histoslider.image.mask_type import MaskType
from histoslider.loaders.loader import Loader
from histoslider.models.base_data import BaseData


class Mask(BaseData):
    def __init__(self, label: str, path: str, mask_type: MaskType, loader: Type[Loader]):
        super().__init__(label)

        self._image = None
        self.path: str = path
        self.mask_type: MaskType = mask_type
        self.loader: Type[Loader] = loader
        self.loaded: bool = False

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def foreground(self):
        return QBrush(Qt.black) if self.loaded else QBrush(Qt.gray)

    @property
    def tooltip(self):
        return "Mask"

    @property
    def image(self):
        if self._image is None:
            return np.zeros((1, 1))
        return self._image

    def load(self):
        if self.loaded or self.loader is None:
            return
        self.loader.load(self)
        self.loaded = True

    def close(self):
        if not self.loaded:
            return
        self.meta = None
        self.clear()
        self.loaded = False

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_children'].clear()
        state['loaded'] = False
        return state
