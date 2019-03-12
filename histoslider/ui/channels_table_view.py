from typing import List, Dict

from PyQt5.QtCore import QSortFilterProxyModel, QItemSelection, Qt
from PyQt5.QtWidgets import QTableView, QHeaderView

from histoslider.core.manager import Manager
from histoslider.core.message import SelectedChannelsChangedMessage
from histoslider.models.channel import Channel
from histoslider.models.channels_model import ChannelsModel


class ChannelsTableView(QTableView):
    def __init__(self, parent):
        QTableView.__init__(self, parent)
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setModel(proxy_model)
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(10)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.sortByColumn(1, Qt.AscendingOrder)
        self.setSortingEnabled(True)
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def set_channels(self, channels: List[Channel]):
        model = ChannelsModel(channels)
        self.model().setSourceModel(model)

    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        proxy_model: QSortFilterProxyModel = self.model()
        model = proxy_model.sourceModel()
        selected_channels: Dict[str, Channel] = dict()
        for index in self.selectedIndexes():
            if index.column() != 0:
                continue
            if index.isValid():
                source_index = proxy_model.mapToSource(index)
                row = source_index.row()
                channel = model.channels[row]
                selected_channels[channel.name] = channel
        if len(selected_channels) < 17:
            Manager.hub.broadcast(SelectedChannelsChangedMessage(self, selected_channels))
