from __future__ import annotations

from PyQt5.QtGui import QIcon

from histoslider.models.base_data import BaseData
from histoslider.models.roi_point_meta import ROIPointMeta


class ROIPoint(BaseData):
    def __init__(self, meta: ROIPointMeta):
        super().__init__(str(meta.order_number))
        self.meta = meta

    @property
    def acquisition_roi(self) -> "AcquisitionROI":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "ROI Point"
