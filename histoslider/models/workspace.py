from typing import List

import jsonpickle

from histoslider.models.base_data import BaseData
from histoslider.slides.mcd.mcd_slide import McdSlide


class Workspace(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_slide(self, slide: McdSlide):
        self.addChild(slide)

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json):
        return jsonpickle.decode(json)

    @property
    def slides(self) -> List[McdSlide]:
        return self._children
