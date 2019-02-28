from dataclasses import dataclass
from typing import Dict, Optional

from dacite import from_dict, Config


@dataclass
class SlideMeta:
    id: int
    uid: str
    description: str
    slide_type: str
    filename: str
    image_file: Optional[str]
    width_um: int
    height_um: int
    image_start_offset: int
    image_end_offset: int

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=SlideMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'uid': 'UID',
                                                'description': 'Description',
                                                'slide_type': 'SlideType',
                                                'filename': 'Filename',
                                                'image_file': 'ImageFile',
                                                'width_um': 'WidthUm',
                                                'height_um': 'HeightUm',
                                                'image_start_offset': 'ImageStartOffset',
                                                'image_end_offset': 'ImageEndOffset'
                                                },
                                         cast=['id',
                                               'width_um',
                                               'height_um',
                                               'image_start_offset',
                                               'image_end_offset'
                                               ]
                                         ))
        return result
