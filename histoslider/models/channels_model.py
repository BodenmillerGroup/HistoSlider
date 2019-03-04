from typing import Dict

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class ChannelsModel(QAbstractTableModel):

    header = ("Name", "Metall", "Mass")

    def __init__(self, channels: Dict, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._channels = channels

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self._channels[index.row()].get(self.keys[index.column()])

    def headerData(self, col: int, orientation: int, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, parent):
        return len(self._channels)

    def columnCount(self, parent):
        return len(self._channels)
