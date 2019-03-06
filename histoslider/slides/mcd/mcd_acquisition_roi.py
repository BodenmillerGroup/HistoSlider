from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.slides.mcd.mcd_acquisition import McdAcquisition
from histoslider.models.base_data import BaseData
from histoslider.slides.mcd.mcd_roi_point import McdROIPoint


class McdAcquisitionROI(BaseData):
    def __init__(self, label: str, meta: dict, roi_points: List[McdROIPoint]):
        super().__init__(label, meta)
        self.roi_points: List[McdROIPoint] = roi_points

    def add_acquisition(self, acquisition: McdAcquisition):
        self.addChild(acquisition)

    @property
    def panorama(self) -> "McdPanorama":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Acquisition ROI"

    @property
    def acquisitions(self) -> List[McdAcquisition]:
        return self._children
