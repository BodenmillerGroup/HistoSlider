from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.slides.mcd.mcd_channel import McdChannel
from histoslider.slides.mcd.mcd_acquisition_meta import McdAcquisitionMeta
from histoslider.models.base_data import BaseData


class McdAcquisition(BaseData):
    def __init__(self, meta: McdAcquisitionMeta):
        super().__init__(meta.description)
        self.meta = meta

    def add_channel(self, channel: McdChannel):
        self.addChild(channel)

    @property
    def acquisition_roi(self) -> "AcquisitionROI":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Acquisition"

    @property
    def channels(self) -> List[McdChannel]:
        return self._children
