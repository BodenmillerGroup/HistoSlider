from __future__ import annotations

from typing import List

from PyQt5.QtGui import QIcon

from histoslider.models.channel import Channel
from histoslider.models.base_data import BaseData


class Acquisition(BaseData):
    def __init__(self, label: str, meta: dict):
        super().__init__(label, meta)
        self._channels: List[Channel] = []

    def add_channel(self, channel: Channel):
        self._channels.append(channel)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Acquisition"

    @property
    def channels(self) -> List[Channel]:
        return self._channels

    @property
    def id(self):
        return self.meta["ID"]
