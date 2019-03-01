from dataclasses import dataclass
from typing import Dict

from dacite import from_dict, Config


@dataclass
class AcquisitionROIMeta:
    id: int
    panorama_id: int
    roi_type: str

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=AcquisitionROIMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'panorama_id': 'PanoramaID',
                                                'roi_type': 'ROIType'
                                                },
                                         cast=['id',
                                               'panorama_id'
                                               ]
                                         ))
        return result
