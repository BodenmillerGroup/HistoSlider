from typing import List

import jsonpickle

from histoslider.models.base_data import BaseData
from histoslider.models.slide import Slide


class Workspace(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_slide(self, slide: Slide):
        self.addChild(slide)

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json):
        return jsonpickle.decode(json)

    @property
    def slides(self) -> List[Slide]:
        return self._children
