from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.slides.mcd.mcd_acquisition import McdAcquisition
from histoslider.slides.mcd.acquisition_roi_meta import AcquisitionROIMeta
from histoslider.models.base_data import BaseData
from histoslider.slides.mcd.roi_point_meta import ROIPointMeta


class AcquisitionROI(BaseData):
    def __init__(self, meta: AcquisitionROIMeta, roi_points: List[ROIPointMeta]):
        super().__init__(meta.roi_type)
        self.meta: AcquisitionROIMeta = meta
        self.roi_points: List[ROIPointMeta] = roi_points

    def add_acquisition(self, acquisition: McdAcquisition):
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
    def acquisitions(self) -> List[McdAcquisition]:
        return self._children
