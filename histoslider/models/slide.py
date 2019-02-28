from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.image.slide_type import SlideType
from histoslider.models.base_data import BaseData
from histoslider.models.panorama import Panorama
from histoslider.models.slide_meta import SlideMeta


class Slide(BaseData):
    def __init__(self, meta: SlideMeta, file_path: str, slide_type: SlideType):
        super().__init__(meta.description)
        self.meta = meta
        self.file_path = file_path
        self.slide_type = slide_type

    def add_panorama(self, panorama: Panorama):
        self.addChild(panorama)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "Slide"

    @property
    def panoramas(self) -> List[Panorama]:
        return self._children
