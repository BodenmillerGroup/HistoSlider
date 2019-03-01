from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon
from imctools.io.imcacquisition import ImcAcquisition

from histoslider.models.base_data import BaseData
from histoslider.slides.ome_tiff.ome_tiff_channel import OmeTiffChannel


class OmeTiffAcquisition(BaseData):
    def __init__(self, imc_acquisition: ImcAcquisition):
        super().__init__(imc_acquisition.image_ID)
        self.imc_acquisition = imc_acquisition

    def add_channel(self, channel: OmeTiffChannel):
        self.addChild(channel)

    @property
    def slide(self) -> "OmeTiffSlide":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "OME-TIFF Acquisition"

    @property
    def channels(self) -> List[OmeTiffChannel]:
        return self._children
