from __future__ import annotations

from PyQt5.QtGui import QIcon

from histoslider.image.slide_type import SlideType
from histoslider.models.base_data import BaseData


class Slide(BaseData):
    def __init__(self, label: str, slide_path: str, slide_type: SlideType):
        super().__init__(label)
        self.slide_path: str = slide_path
        self.slide_type: SlideType = slide_type
        self.loaded: bool = False

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "Slide"

    def load(self):
        self.loaded = True

    def unload(self):
        self.clear()
        self.loaded = False

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_children'].clear()
        state['loaded'] = False
        return state
