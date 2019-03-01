from dataclasses import dataclass
from typing import Dict, List

from dacite import from_dict, Config


@dataclass
class OmeTiffSlideMeta:
    image_id: str
    channel_metals: List[str]
    channel_labels: List[str]

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=OmeTiffSlideMeta, data=data,
                           config=Config(remap={'image_id': 'image_ID'}
                                         ))
        return result
