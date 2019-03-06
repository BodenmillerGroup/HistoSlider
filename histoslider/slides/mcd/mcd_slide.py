from __future__ import annotations

import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from imctools.io import mcdparser

from histoslider.image.slide_type import SlideType
from histoslider.models.slide import Slide
from histoslider.slides.mcd.mcd_acquisition import McdAcquisition
from histoslider.slides.mcd.mcd_channel import McdChannel
from histoslider.slides.mcd.mcd_acquisition_roi import McdAcquisitionROI
from histoslider.slides.mcd.mcd_panorama import McdPanorama
from histoslider.slides.mcd.mcd_roi_point import McdROIPoint


class McdSlide(Slide):
    def __init__(self, slide_path: str):
        file_name = os.path.basename(slide_path)
        super().__init__(file_name, slide_path, SlideType.MCD)

    @property
    def tooltip(self):
        return "MCD Slide"

    @property
    def foreground(self):
        return QBrush(Qt.black) if self.loaded else QBrush(Qt.gray)

    def add_panorama(self, panorama: McdPanorama):
        self.addChild(panorama)

    @property
    def panoramas(self) -> List[McdPanorama]:
        return self._children

    def load(self):
        if self.loaded:
            return
        with mcdparser.McdParser(self.slide_path) as mcd:
            slide_item = mcd.meta.objects['Slide']['0']
            self.meta = slide_item.properties
            for panorama_item in slide_item.childs['Panorama'].values():
                panorama = McdPanorama(panorama_item.properties['Description'], panorama_item.properties)
                self.add_panorama(panorama)
                if 'AcquisitionROI' in panorama_item.childs:
                    for acquisition_roi_item in panorama_item.childs['AcquisitionROI'].values():
                        roi_points: List[McdROIPoint] = list()
                        for roi_point_item in acquisition_roi_item.childs['ROIPoint'].values():
                            roi_point = McdROIPoint(roi_point_item.metaname, roi_point_item.properties)
                            roi_points.append(roi_point)
                        acquisition_roi = McdAcquisitionROI(acquisition_roi_item.metaname, acquisition_roi_item.properties, roi_points)
                        panorama.add_acquisition_roi(acquisition_roi)
                        for acquisition_item in acquisition_roi_item.childs['Acquisition'].values():
                            # Dict key should be str!
                            acquisition = McdAcquisition(acquisition_item.properties['Description'], acquisition_item.properties)
                            acquisition_roi.add_acquisition(acquisition)
                            channel_list = list(acquisition_item.childs['AcquisitionChannel'].values())
                            imc_acquisition = mcd.get_imc_acquisition(acquisition.id)
                            for i in range(imc_acquisition.n_channels):
                                img = imc_acquisition.get_img_by_label(imc_acquisition.channel_labels[i])
                                ch = channel_list[i]
                                meta = ch.properties.copy()
                                meta['Metal'] = imc_acquisition.channel_metals[i]
                                meta['Mass'] = imc_acquisition.channel_mass[i]
                                channel = McdChannel(meta['ChannelLabel'], meta, img)
                                acquisition.add_channel(channel)
        super().load()

    def unload(self):
        if not self.loaded:
            return
        self.meta = None
        super().unload()
