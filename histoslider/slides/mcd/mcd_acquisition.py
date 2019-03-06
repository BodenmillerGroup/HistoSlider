from __future__ import annotations

from typing import List

from histoslider.models.acquisition import Acquisition
from histoslider.slides.mcd.mcd_channel import McdChannel


class McdAcquisition(Acquisition):
    def __init__(self, label: str, meta: dict):
        super().__init__(label, meta)

    def add_channel(self, channel: McdChannel):
        self.addChild(channel)

    @property
    def acquisition_roi(self) -> "McdAcquisitionROI":
        return self.parent()

    @property
    def channels(self) -> List[McdChannel]:
        return self._children

    @property
    def id(self):
        return self.meta["ID"]
