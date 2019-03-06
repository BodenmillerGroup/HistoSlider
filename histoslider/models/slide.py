from __future__ import annotations

from typing import Type

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush

from histoslider.image.slide_type import SlideType
from histoslider.loaders.loader import Loader
from histoslider.models.base_data import BaseData


class Slide(BaseData):
    def __init__(self, label: str, slide_path: str, slide_type: SlideType, loader: Type[Loader]):
        super().__init__(label)

        self.slide_path: str = slide_path
        self.slide_type: SlideType = slide_type
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
        return "Slide"

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
