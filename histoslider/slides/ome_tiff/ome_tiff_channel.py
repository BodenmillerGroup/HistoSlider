from __future__ import annotations

from numpy.core.multiarray import ndarray

from histoslider.models.channel import Channel


class OmeTiffChannel(Channel):
    def __init__(self, label: str, metal: str, mass: float, image: ndarray):
        super().__init__(label, metal, mass, image)

    @property
    def acquisition(self) -> "OmeTiffAcquisition":
        return self.parent()

    @property
    def tooltip(self):
        return "OME-TIFF Channel"
