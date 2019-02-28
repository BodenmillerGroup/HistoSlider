from typing import List

import imctools.io.mcdparser as mcdparser

from histoslider.image.slide_type import SlideType
from histoslider.models.acquisition import Acquisition
from histoslider.models.acquisition_channel_meta import AcquisitionChannelMeta
from histoslider.models.acquisition_meta import AcquisitionMeta
from histoslider.models.acquisition_channel import AcquisitionChannel
from histoslider.models.acquisition_roi import AcquisitionROI
from histoslider.models.acquisition_roi_meta import AcquisitionROIMeta
from histoslider.models.panorama import Panorama
from histoslider.models.panorama_meta import PanoramaMeta
from histoslider.models.roi_point import ROIPoint
from histoslider.models.roi_point_meta import ROIPointMeta
from histoslider.models.slide import Slide
from histoslider.models.slide_meta import SlideMeta


class McdLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        with mcdparser.McdParser(self.file_path) as mcd:
            slide_item = mcd.meta.objects['Slide']['0']
            slide_meta = SlideMeta.from_dict(slide_item.properties)
            slide = Slide(slide_meta, self.file_path, SlideType.MCD)
            for panorama_item in slide_item.childs['Panorama'].values():
                panorama_meta = PanoramaMeta.from_dict(panorama_item.properties)
                panorama = Panorama(panorama_meta)
                slide.add_panorama(panorama)
                for acquisition_roi_item in panorama_item.childs['AcquisitionROI'].values():
                    acquisition_roi_meta = AcquisitionROIMeta.from_dict(acquisition_roi_item.properties)
                    roi_points: List[ROIPointMeta] = list()
                    for roi_point_item in acquisition_roi_item.childs['ROIPoint'].values():
                        roi_point_meta = ROIPointMeta.from_dict(roi_point_item.properties)
                        roi_points.append(roi_point_meta)
                    acquisition_roi = AcquisitionROI(acquisition_roi_meta, roi_points)
                    panorama.add_acquisition_roi(acquisition_roi)
                    for acquisition_item in acquisition_roi_item.childs['Acquisition'].values():
                        acquisition_meta = AcquisitionMeta.from_dict(acquisition_item.properties)
                        # Dict key should be str!
                        imc_acquisition = mcd.get_imc_acquisition(str(acquisition_meta.id))
                        acquisition = Acquisition(acquisition_meta)
                        acquisition_roi.add_acquisition(acquisition)
                        channel_list = list(acquisition_item.childs['AcquisitionChannel'].values())
                        for i in range(imc_acquisition.n_channels):
                            acquisition_channel_meta = AcquisitionChannelMeta.from_dict(channel_list[i].properties)
                            img = imc_acquisition.get_img_by_label(imc_acquisition.channel_labels[i])
                            acquisition_channel = AcquisitionChannel(acquisition_channel_meta, imc_acquisition.channel_metals[i],
                                              imc_acquisition.channel_mass[i], img)
                            acquisition.add_channel(acquisition_channel)
            return slide
