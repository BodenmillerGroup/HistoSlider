from dataclasses import dataclass
from typing import Dict

from dacite import from_dict, Config


@dataclass
class PanoramaMeta:
    id: int
    slide_id: int
    description: str
    image_format: str
    pixel_scale_coef: float
    pixel_width: int
    pixel_height: int
    image_start_offset: int
    image_end_offset: int
    slide_x1_pos_um: float
    slide_y1_pos_um: float
    slide_x2_pos_um: float
    slide_y2_pos_um: float
    slide_x3_pos_um: float
    slide_y3_pos_um: float
    slide_x4_pos_um: float
    slide_y4_pos_um: float

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=PanoramaMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'slide_id': 'SlideID',
                                                'description': 'Description',
                                                'image_format': 'ImageFormat',
                                                'pixel_scale_coef': 'PixelScaleCoef',
                                                'pixel_width': 'PixelWidth',
                                                'pixel_height': 'PixelHeight',
                                                'image_start_offset': 'ImageStartOffset',
                                                'image_end_offset': 'ImageEndOffset',
                                                'slide_x1_pos_um': 'SlideX1PosUm',
                                                'slide_y1_pos_um': 'SlideY1PosUm',
                                                'slide_x2_pos_um': 'SlideX2PosUm',
                                                'slide_y2_pos_um': 'SlideY2PosUm',
                                                'slide_x3_pos_um': 'SlideX3PosUm',
                                                'slide_y3_pos_um': 'SlideY3PosUm',
                                                'slide_x4_pos_um': 'SlideX4PosUm',
                                                'slide_y4_pos_um': 'SlideY4PosUm'
                                                },
                                         cast=['id',
                                               'slide_id',
                                               'pixel_scale_coef',
                                               'pixel_width',
                                               'pixel_height',
                                               'image_start_offset',
                                               'image_end_offset',
                                               'slide_x1_pos_um',
                                               'slide_y1_pos_um',
                                               'slide_x2_pos_um',
                                               'slide_y2_pos_um',
                                               'slide_x3_pos_um',
                                               'slide_y3_pos_um',
                                               'slide_x4_pos_um',
                                               'slide_y4_pos_um'
                                               ]
                                         ))
        return result
