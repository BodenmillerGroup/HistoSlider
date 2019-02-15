from typing import List

from PyQt5.QtGui import QIcon

from histoslider.models.base_data import BaseData
from histoslider.models.channel import Channel


class Acquisition(BaseData):
    def __init__(self, name: str, description: str):
        super().__init__(name)
        self.description = description

    def add_channel(self, channel: Channel):
        self.addChild(channel)

    @property
    def slide(self):
        return self.parent()

    @property
    def icon(self):
        return QIcon(":/icons/icons8-film-roll-16.png")

    @property
    def tooltip(self):
        return "Acquisition"

    @property
    def channels(self) -> List[Channel]:
        return self._children
