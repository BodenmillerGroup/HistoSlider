from __future__ import annotations

import os
from typing import List

from imctools.io import mcdparser

from histoslider.loaders.loader import Loader
from histoslider.models.acquisition import Acquisition
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide
from histoslider.models.acquisition_roi import AcquisitionROI
from histoslider.models.panorama import Panorama
from histoslider.models.roi_point import ROIPoint


class McdLoader(Loader):

    @classmethod
    def load(cls, slide: Slide) -> Slide:
        slide_path = slide.slide_path
        with mcdparser.McdParser(slide_path) as mcd:
            slide_item = mcd.meta.objects['Slide']['0']
            file_name = os.path.basename(slide_path)
            slide.meta = slide_item.properties
            for panorama_item in slide_item.childs['Panorama'].values():
                panorama = Panorama(panorama_item.properties['Description'], panorama_item.properties)
                slide.addChild(panorama)
                if 'AcquisitionROI' in panorama_item.childs:
                    for acquisition_roi_item in panorama_item.childs['AcquisitionROI'].values():
                        roi_points: List[ROIPoint] = list()
                        for roi_point_item in acquisition_roi_item.childs['ROIPoint'].values():
                            roi_point = ROIPoint(roi_point_item.metaname, roi_point_item.properties)
                            roi_points.append(roi_point)
                        acquisition_roi = AcquisitionROI(acquisition_roi_item.metaname, acquisition_roi_item.properties, roi_points)
                        panorama.add_acquisition_roi(acquisition_roi)
                        for acquisition_item in acquisition_roi_item.childs['Acquisition'].values():
                            # Dict key should be str!
                            acquisition = Acquisition(acquisition_item.properties['Description'], acquisition_item.properties)
                            acquisition_roi.add_acquisition(acquisition)
                            imc_acquisition = mcd.get_imc_acquisition(acquisition.id)
                            for i in range(imc_acquisition.n_channels):
                                meta = dict()
                                label = imc_acquisition.channel_labels[i]
                                meta['Label'] = label
                                meta['Metal'] = imc_acquisition.channel_metals[i]
                                meta['Mass'] = imc_acquisition.channel_mass[i]
                                img = imc_acquisition.get_img_by_label(label)
                                channel = Channel(label, meta, img)
                                acquisition.add_channel(channel)
            return slide

    @classmethod
    def close(cls, slide: Slide):
        raise NotImplementedError
