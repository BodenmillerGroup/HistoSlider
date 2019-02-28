from __future__ import annotations

from PyQt5.QtGui import QIcon
from numpy.core.multiarray import ndarray

from histoslider.models.acquisition_channel_meta import AcquisitionChannelMeta
from histoslider.models.base_data import BaseData


class AcquisitionChannel(BaseData):
    def __init__(self, meta: AcquisitionChannelMeta, metal: str, mass: float, image: ndarray):
        super().__init__(meta.channel_label)
        self.meta = meta
        self.metal = metal
        self.mass = mass
        self.image = image

    @property
    def acquisition(self) -> "Acquisition":
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-compact-camera-16.png")

    @property
    def tooltip(self):
        return "Acquisition channel"
