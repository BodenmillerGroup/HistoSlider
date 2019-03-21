from typing import List

from histoslider.models.base_data import BaseData
from histoslider.models.mask import Mask
from histoslider.models.slide import Slide


class Workspace(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_slide(self, slide: Slide):
        self.addChild(slide)

    def add_mask(self, mask: Mask):
        self.addChild(mask)

    @property
    def slides(self) -> List[Slide]:
        return [child for child in self._children if isinstance(child, Slide)]

    @property
    def masks(self) -> List[Mask]:
        return [child for child in self._children if isinstance(child, Mask)]
