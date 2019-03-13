from typing import List, Tuple

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class ChannelsModel(QAbstractTableModel):

    header = ('Label', 'Metal', 'Mass')

    def __init__(self, channels: List[Tuple[str, str, float]], parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.channels = channels

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        item = self.channels[index.row()]
        return item[index.column()]

    def headerData(self, col: int, orientation: int, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, parent):
        return len(self.channels)

    def columnCount(self, parent):
        return len(self.header)
