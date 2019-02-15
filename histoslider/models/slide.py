from typing import List

from PyQt5.QtGui import QIcon

from histoslider.image.slide_type import SlideType
from histoslider.models.acquisition import Acquisition
from histoslider.models.base_data import BaseData


class Slide(BaseData):
    def __init__(self, name: str, path: str, slide_type: SlideType):
        super().__init__(name)
        self.path = path
        self.slide_type = slide_type

    def add_acquisition(self, acquisition: Acquisition):
        self.addChild(acquisition)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "Slide"

    @property
    def acquisitions(self) -> List[Acquisition]:
        return self._children
