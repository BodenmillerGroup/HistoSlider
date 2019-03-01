from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from dacite import from_dict, Config
from dateutil import parser


@dataclass
class McdAcquisitionMeta:
    id: int
    acquisition_roi_id: int
    description: str
    template: str
    signal_type: str
    movement_type: str
    order_number: int
    segment_data_format: str
    value_bytes: int
    dual_count_start: int
    data_start_offset: int
    data_end_offset: int
    start_time_stamp: datetime
    end_time_stamp: datetime
    max_x: int
    max_y: int
    plume_start: int
    plume_end: int
    ablation_power: float
    ablation_frequency: float
    ablation_distance_between_shots_x: float
    ablation_distance_between_shots_y: float
    before_ablation_image_start_offset: int
    before_ablation_image_end_offset: int
    after_ablation_image_start_offset: int
    after_ablation_image_end_offset: int
    roi_start_x_pos_um: float
    roi_start_y_pos_um: float
    roi_end_x_pos_um: float
    roi_end_y_pos_um: float

    @staticmethod
    def from_dict(data: Dict):
        result = from_dict(data_class=McdAcquisitionMeta, data=data,
                           config=Config(remap={'id': 'ID',
                                                'acquisition_roi_id': 'AcquisitionROIID',
                                                'description': 'Description',
                                                'template': 'Template',
                                                'signal_type': 'SignalType',
                                                'movement_type': 'MovementType',
                                                'order_number': 'OrderNumber',
                                                'segment_data_format': 'SegmentDataFormat',
                                                'value_bytes': 'ValueBytes',
                                                'dual_count_start': 'DualCountStart',
                                                'data_start_offset': 'DataStartOffset',
                                                'data_end_offset': 'DataEndOffset',
                                                'start_time_stamp': 'StartTimeStamp',
                                                'end_time_stamp': 'EndTimeStamp',
                                                'max_x': 'MaxX',
                                                'max_y': 'MaxY',
                                                'plume_start': 'PlumeStart',
                                                'plume_end': 'PlumeEnd',
                                                'ablation_power': 'AblationPower',
                                                'ablation_frequency': 'AblationFrequency',
                                                'ablation_distance_between_shots_x': 'AblationDistanceBetweenShotsX',
                                                'ablation_distance_between_shots_y': 'AblationDistanceBetweenShotsY',
                                                'before_ablation_image_start_offset': 'BeforeAblationImageStartOffset',
                                                'before_ablation_image_end_offset': 'BeforeAblationImageEndOffset',
                                                'after_ablation_image_start_offset': 'AfterAblationImageStartOffset',
                                                'after_ablation_image_end_offset': 'AfterAblationImageEndOffset',
                                                'roi_start_x_pos_um': 'ROIStartXPosUm',
                                                'roi_start_y_pos_um': 'ROIStartYPosUm',
                                                'roi_end_x_pos_um': 'ROIEndXPosUm',
                                                'roi_end_y_pos_um': 'ROIEndYPosUm'
                                                },
                                         cast=['id',
                                               'acquisition_roi_id',
                                               'order_number',
                                               'value_bytes',
                                               'dual_count_start',
                                               'data_start_offset',
                                               'data_end_offset',
                                               'max_x',
                                               'max_y',
                                               'plume_start',
                                               'plume_end',
                                               'ablation_power',
                                               'ablation_frequency',
                                               'ablation_distance_between_shots_x',
                                               'ablation_distance_between_shots_y',
                                               'before_ablation_image_start_offset',
                                               'before_ablation_image_end_offset',
                                               'after_ablation_image_start_offset',
                                               'after_ablation_image_end_offset',
                                               'roi_start_x_pos_um',
                                               'roi_start_y_pos_um',
                                               'roi_end_x_pos_um',
                                               'roi_end_y_pos_um'
                                               ],
                                         transform={'start_time_stamp': parser.parse,
                                                    'end_time_stamp': parser.parse}
                                         ))
        return result
