from __future__ import annotations

import os

from PyQt5.QtGui import QIcon

from histoslider.image.slide_type import SlideType
from histoslider.models.slide import Slide


class TiffSlide(Slide):
    def __init__(self, slide_path: str):
        file_name = os.path.basename(slide_path)
        super().__init__(file_name, slide_path, SlideType.TIFF)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "TIFF Slide"

    def load(self):
        if self.loaded:
            return
        super().load()

    def unload(self):
        if not self.loaded:
            return
        super().unload()
