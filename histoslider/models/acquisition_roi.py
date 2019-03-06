from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.models.acquisition import Acquisition
from histoslider.models.base_data import BaseData
from histoslider.models.roi_point import ROIPoint


class AcquisitionROI(BaseData):
    def __init__(self, label: str, meta: dict, roi_points: List[ROIPoint]):
        super().__init__(label, meta)
        self.roi_points: List[ROIPoint] = roi_points

    def add_acquisition(self, acquisition: Acquisition):
        self.addChild(acquisition)

    @property
    def panorama(self) -> "Panorama":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Acquisition ROI"

    @property
    def acquisitions(self) -> List[Acquisition]:
        return self._children
