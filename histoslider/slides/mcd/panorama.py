from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.slides.mcd.acquisition_roi import AcquisitionROI
from histoslider.models.base_data import BaseData
from histoslider.slides.mcd.panorama_meta import PanoramaMeta


class Panorama(BaseData):
    def __init__(self, meta: PanoramaMeta):
        super().__init__(meta.description)
        self.meta = meta

    def add_acquisition_roi(self, acquisition_roi: AcquisitionROI):
        self.addChild(acquisition_roi)

    @property
    def slide(self) -> "McdSlide":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Panorama"

    @property
    def acquisition_rois(self) -> List[AcquisitionROI]:
        return self._children
