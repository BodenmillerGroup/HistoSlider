from __future__ import annotations

from numpy.core.multiarray import ndarray

from histoslider.models.channel import Channel
from histoslider.slides.mcd.mcd_channel_meta import McdChannelMeta


class McdChannel(Channel):
    def __init__(self, meta: McdChannelMeta, metal: str, mass: float, image: ndarray):
        super().__init__(meta.channel_label, metal, mass, image)
        self.meta = meta

    @property
    def acquisition(self) -> "McdAcquisition":
        return self.parent()

    @property
    def tooltip(self):
        return "MCD Channel"
