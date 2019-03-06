from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.slides.mcd.mcd_acquisition_roi import McdAcquisitionROI
from histoslider.models.base_data import BaseData


class McdPanorama(BaseData):
    def __init__(self, label: str, meta: dict):
        super().__init__(label, meta)
        self.meta = meta

    def add_acquisition_roi(self, acquisition_roi: McdAcquisitionROI):
        self.addChild(acquisition_roi)

    @property
    def slide(self) -> "McdSlide":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "MCD Panorama"

    @property
    def acquisition_rois(self) -> List[McdAcquisitionROI]:
        return self._children
