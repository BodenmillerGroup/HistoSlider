from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.models.acquisition import Acquisition
from histoslider.models.acquisition_roi_meta import AcquisitionROIMeta
from histoslider.models.base_data import BaseData
from histoslider.models.roi_point_meta import ROIPointMeta


class AcquisitionROI(BaseData):
    def __init__(self, meta: AcquisitionROIMeta, roi_points: List[ROIPointMeta]):
        super().__init__(meta.roi_type)
        self.meta: AcquisitionROIMeta = meta
        self.roi_points: List[ROIPointMeta] = roi_points

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
