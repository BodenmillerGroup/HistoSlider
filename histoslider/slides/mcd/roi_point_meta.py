from dataclasses import dataclass
from typing import Dict

from dacite import from_dict, Config


@dataclass
class ROIPointMeta:
    id: int
    acquisition_roi_id: int
    order_number: int
    slide_x_pos_um: int
    slide_y_pos_um: int
    panorama_pixel_x_pos: int
    panorama_pixel_y_pos: int

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=ROIPointMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'acquisition_roi_id': 'AcquisitionROIID',
                                                'order_number': 'OrderNumber',
                                                'slide_x_pos_um': 'SlideXPosUm',
                                                'slide_y_pos_um': 'SlideYPosUm',
                                                'panorama_pixel_x_pos': 'PanoramaPixelXPos',
                                                'panorama_pixel_y_pos': 'PanoramaPixelYPos'
                                                },
                                         cast=['id',
                                               'acquisition_roi_id',
                                               'order_number',
                                               'slide_x_pos_um',
                                               'slide_y_pos_um',
                                               'panorama_pixel_x_pos',
                                               'panorama_pixel_y_pos'
                                               ]
                                         ))
        return result
