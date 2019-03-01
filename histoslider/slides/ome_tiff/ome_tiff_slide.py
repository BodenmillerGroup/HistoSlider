from __future__ import annotations

import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush
from imctools.io.ometiffparser import OmetiffParser

from histoslider.image.slide_type import SlideType
from histoslider.models.slide import Slide
from histoslider.slides.ome_tiff.ome_tiff_acquisition import OmeTiffAcquisition
from histoslider.slides.ome_tiff.ome_tiff_channel import OmeTiffChannel
from histoslider.slides.ome_tiff.ome_tiff_slide_meta import OmeTiffSlideMeta


class OmeTiffSlide(Slide):
    def __init__(self, slide_path: str):
        file_name = os.path.basename(slide_path)
        super().__init__(file_name, slide_path, SlideType.OMETIFF)
        self.meta: OmeTiffSlideMeta = None

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "OME-TIFF Slide"

    @property
    def foreground(self):
        return QBrush(Qt.black) if self.loaded else QBrush(Qt.gray)

    def add_acquisition(self, acquisition: OmeTiffAcquisition):
        self.addChild(acquisition)

    @property
    def acquisitions(self) -> List[OmeTiffAcquisition]:
        return self._children

    def load(self):
        if self.loaded:
            return
        ome = OmetiffParser(self.slide_path)
        self.meta = OmeTiffSlideMeta.from_dict(ome.meta_dict)
        imc_acquisition = ome.get_imc_acquisition()
        acquisition = OmeTiffAcquisition(imc_acquisition)
        self.add_acquisition(acquisition)
        for i in range(imc_acquisition.n_channels):
            img = imc_acquisition.get_img_by_label(imc_acquisition.channel_labels[i])
            channel = OmeTiffChannel(imc_acquisition.channel_labels[i], imc_acquisition.channel_metals[i], imc_acquisition.channel_mass[i], img)
            acquisition.add_channel(channel)
        super().load()

    def unload(self):
        if not self.loaded:
            return
        self.meta = None
        self.clear()
        super().unload()
