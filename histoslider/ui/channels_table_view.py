from typing import List, Set, Tuple

from PyQt5.QtCore import QSortFilterProxyModel, QItemSelection, Qt
from PyQt5.QtWidgets import QTableView, QHeaderView

from histoslider.core.manager import Manager
from histoslider.core.message import SelectedMetalsChangedMessage
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

        self.channel_list: List[Tuple[str, str, int]] = None

    def clear(self):
        self.model().setSourceModel(None)
        self.channel_list = None

    def set_channels(self, channels: List[Channel]):
        new_channel_list = list()
        for c in channels:
            new_channel_list.append((c.label, c.metal, c.mass))
        if new_channel_list != self.channel_list:
            self.channel_list = new_channel_list
            model = ChannelsModel(self.channel_list)
            self.model().setSourceModel(model)

    def _on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        proxy_model: QSortFilterProxyModel = self.model()
        model = proxy_model.sourceModel()
        selected_metals: Set[str] = set()
        for index in self.selectedIndexes():
            if index.column() != 0:
                continue
            if index.isValid():
                source_index = proxy_model.mapToSource(index)
                row = source_index.row()
                channel = model.channels[row]
                selected_metals.add(channel[1])
        if len(selected_metals) < 7:
            Manager.hub.broadcast(SelectedMetalsChangedMessage(self, selected_metals))
