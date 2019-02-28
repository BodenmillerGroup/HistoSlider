from dataclasses import dataclass
from typing import Dict

from dacite import from_dict, Config


@dataclass
class AcquisitionChannelMeta:
    id: int
    acquisition_id: int
    order_number: int
    channel_name: str
    channel_label: str


    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=AcquisitionChannelMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'acquisition_id': 'AcquisitionID',
                                                'order_number': 'OrderNumber',
                                                'channel_name': 'ChannelName',
                                                'channel_label': 'ChannelLabel'
                                                },
                                         cast=['id',
                                               'acquisition_id',
                                               'order_number'
                                               ]
                                         ))
        return result
