from __future__ import annotations

import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush
from imctools.io import mcdparser

from histoslider.image.slide_type import SlideType
from histoslider.models.slide import Slide
from histoslider.slides.mcd.mcd_acquisition import McdAcquisition
from histoslider.slides.mcd.mcd_channel import McdChannel
from histoslider.slides.mcd.mcd_channel_meta import McdChannelMeta
from histoslider.slides.mcd.mcd_acquisition_meta import McdAcquisitionMeta
from histoslider.slides.mcd.acquisition_roi import AcquisitionROI
from histoslider.slides.mcd.acquisition_roi_meta import AcquisitionROIMeta
from histoslider.slides.mcd.panorama import Panorama
from histoslider.slides.mcd.mcd_slide_meta import McdSlideMeta
from histoslider.slides.mcd.panorama_meta import PanoramaMeta
from histoslider.slides.mcd.roi_point_meta import ROIPointMeta


class McdSlide(Slide):
    def __init__(self, slide_path: str):
        file_name = os.path.basename(slide_path)
        super().__init__(file_name, slide_path, SlideType.MCD)
        self.meta: McdSlideMeta = None

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "MCD Slide"

    @property
    def foreground(self):
        return QBrush(Qt.black) if self.loaded else QBrush(Qt.gray)

    def add_panorama(self, panorama: Panorama):
        self.addChild(panorama)

    @property
    def panoramas(self) -> List[Panorama]:
        return self._children

    def load(self):
        if self.loaded:
            return
        with mcdparser.McdParser(self.slide_path) as mcd:
            slide_item = mcd.meta.objects['Slide']['0']
            self.meta = McdSlideMeta.from_dict(slide_item.properties)
            for panorama_item in slide_item.childs['Panorama'].values():
                panorama_meta = PanoramaMeta.from_dict(panorama_item.properties)
                panorama = Panorama(panorama_meta)
                self.add_panorama(panorama)
                for acquisition_roi_item in panorama_item.childs['AcquisitionROI'].values():
                    acquisition_roi_meta = AcquisitionROIMeta.from_dict(acquisition_roi_item.properties)
                    roi_points: List[ROIPointMeta] = list()
                    for roi_point_item in acquisition_roi_item.childs['ROIPoint'].values():
                        roi_point_meta = ROIPointMeta.from_dict(roi_point_item.properties)
                        roi_points.append(roi_point_meta)
                    acquisition_roi = AcquisitionROI(acquisition_roi_meta, roi_points)
                    panorama.add_acquisition_roi(acquisition_roi)
                    for acquisition_item in acquisition_roi_item.childs['Acquisition'].values():
                        acquisition_meta = McdAcquisitionMeta.from_dict(acquisition_item.properties)
                        # Dict key should be str!
                        imc_acquisition = mcd.get_imc_acquisition(str(acquisition_meta.id))
                        acquisition = McdAcquisition(acquisition_meta)
                        acquisition_roi.add_acquisition(acquisition)
                        channel_list = list(acquisition_item.childs['AcquisitionChannel'].values())
                        for i in range(imc_acquisition.n_channels):
                            acquisition_channel_meta = McdChannelMeta.from_dict(channel_list[i].properties)
                            img = imc_acquisition.get_img_by_label(imc_acquisition.channel_labels[i])
                            acquisition_channel = McdChannel(acquisition_channel_meta, imc_acquisition.channel_metals[i],
                                                             imc_acquisition.channel_mass[i], img)
                            acquisition.add_channel(acquisition_channel)
        super().load()

    def unload(self):
        if not self.loaded:
            return
        self.meta = None
        super().unload()
