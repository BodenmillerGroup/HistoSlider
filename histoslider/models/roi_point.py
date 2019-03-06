from __future__ import annotations

from PyQt5.QtGui import QIcon

from histoslider.models.base_data import BaseData


class ROIPoint(BaseData):
    def __init__(self, label: str, meta: dict):
        super().__init__(label, meta)

    @property
    def acquisition_roi(self) -> "AcquisitionROI":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "ROI Point"
