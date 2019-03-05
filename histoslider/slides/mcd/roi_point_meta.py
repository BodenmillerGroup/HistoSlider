from dataclasses import dataclass
from typing import Dict

from dacite import from_dict, Config


@dataclass
class ROIPointMeta:
    id: str
    acquisition_roi_id: str
    order_number: str
    slide_x_pos_um: str
    slide_y_pos_um: str
    panorama_pixel_x_pos: str
    panorama_pixel_y_pos: str

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
                                         # cast=['id',
                                         #       'acquisition_roi_id',
                                         #       'order_number',
                                         #       'slide_x_pos_um',
                                         #       'slide_y_pos_um',
                                         #       'panorama_pixel_x_pos',
                                         #       'panorama_pixel_y_pos'
                                         #       ]
                                         ))
        return result
