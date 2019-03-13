from typing import List

from histoslider.models.base_data import BaseData
from histoslider.models.slide import Slide


class Workspace(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_slide(self, slide: Slide):
        self.addChild(slide)

    @property
    def slides(self) -> List[Slide]:
        return self._children
