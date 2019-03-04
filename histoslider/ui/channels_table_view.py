from PyQt5.QtCore import QSortFilterProxyModel, QItemSelection
from PyQt5.QtWidgets import QTableView, QAbstractItemView


class ChannelsTableView(QTableView):
    def __init__(self, parent):
        QTableView.__init__(self, parent)
        channel_model = QSortFilterProxyModel()
        self.setModel(channel_model)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def set_channels(self, channels):
        proxy_model = self.model()
        channel_model = ChannelsModel()
        proxy_model.setSourceModel(channel_model)


    def _on_selection_changed(self, new: QItemSelection, old: QItemSelection):
        model = self.model()
        source_model = model.sourceModel()
        rows = self.selectionModel().selectedRows()
        if len(rows) > 0:
            row = new.indexes()[0]
            row = model.mapToSource(row)
            row = row.row()
