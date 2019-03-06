from __future__ import annotations

from numpy.core.multiarray import ndarray

from histoslider.models.channel import Channel


class McdChannel(Channel):
    def __init__(self, label: str, meta: dict, image: ndarray):
        super().__init__(label, meta, image)

    @property
    def acquisition(self) -> "McdAcquisition":
        return self.parent()

    @property
    def tooltip(self):
        return "MCD Channel"
