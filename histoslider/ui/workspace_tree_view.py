from functools import partial

from PyQt5.QtCore import Qt, QModelIndex, QItemSelection
from PyQt5.QtWidgets import QTreeView, QWidget, QAbstractItemView, QMenu

from histoslider.core.message import SelectedTreeNodeChangedMessage, SelectedAcquisitionChangedMessage
from histoslider.core.manager import Manager
from histoslider.models.acquisition import Acquisition
from histoslider.models.slide import Slide


class WorkspaceTreeView(QTreeView):
    def __init__(self, parent: QWidget = None):
        QTreeView.__init__(self, parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setModel(Manager.data.workspace_model)
        self.customContextMenuRequested.connect(self._open_menu)
        self.selectionModel().selectionChanged.connect(self._treeview_selection_changed)
        self.selectionModel().currentChanged.connect(self._treeview_current_changed)
        self.doubleClicked.connect(self._treeview_double_clicked)

    def _open_menu(self, position):
        indexes = self.selectedIndexes()

        level = None
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu(self)

        if level == 1:
            action = menu.addAction("Load")
            action.triggered.connect(partial(self._load, indexes))

            action = menu.addAction("Close")
            action.triggered.connect(partial(self._close, indexes))

            action = menu.addAction("Remove")
            action.triggered.connect(partial(self._remove, indexes))
        elif level == 2:
            menu.addAction("Edit object/container")
        elif level == 3:
            menu.addAction("Edit object")

        menu.exec_(self.viewport().mapToGlobal(position))

    def _close(self, indexes: [QModelIndex]):
        Manager.close_slides(indexes)

    def _load(self, indexes: [QModelIndex]):
        Manager.load_slides(indexes)

    def _remove(self, indexes: [QModelIndex]):
        Manager.remove_slides(indexes)

    def _treeview_current_changed(self, current: QModelIndex, previous: QModelIndex):
        if current.isValid():
            item = current.model().getItem(current)
            Manager.hub.broadcast(SelectedTreeNodeChangedMessage(self, item))
            if isinstance(item, Acquisition):
                Manager.hub.broadcast(SelectedAcquisitionChangedMessage(self, item))

    def _treeview_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()

    def _treeview_double_clicked(self, index: QModelIndex):
        if index.isValid():
            item = index.model().getItem(index)
            if isinstance(item, Slide) and not item.loaded:
                Manager.load_slides([index])
